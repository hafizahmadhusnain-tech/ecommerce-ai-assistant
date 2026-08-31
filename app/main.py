from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.database.postgres import Base, engine, seed_initial_data
from app.database.chromadb import seed_vector_store_if_needed
from app.api.v1.chat import router as chat_router
from app.api.v1.auth import router as auth_router

# Lifespan manager (Startup & Shutdown events)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create Postgres tables auto-magically if they don't exist
    Base.metadata.create_all(bind=engine)
    # Startup: Auto-seed initial catalog products and sample orders into PostgreSQL
    seed_initial_data()
    # Startup: Seed ChromaDB vector store if empty
    seed_vector_store_if_needed()
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Clean up connections
    await close_mongo_connection()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route Registrations
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/api/v1", tags=["AI Chatbot"])

# 2. Base Route
@app.get("/")
def read_root():
    return {
        "status": "online", 
        "app_name": settings.APP_NAME,
        "environment": "Development" if settings.DEBUG else "Production"
    }

# 3. Gemini Config Validation Check Route (Jo miss ho gaya tha!)
@app.get("/health/ai")
def check_gemini_config():
    if not settings.GEMINI_API_KEY or "ActualGeminiApiKey" in settings.GEMINI_API_KEY:
        return {"status": "error", "message": "Gemini API Key properly set nahi hai ya placeholder use ho raha hai!"}
    return {"status": "configured", "message": "Gemini Key successfully loaded from core configuration."}