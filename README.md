# 🛍️ Nova Store AI - Intelligent E-Commerce Assistant

An autonomous, next-generation AI shopping assistant built with **FastAPI**, **LangChain Google GenAI (Gemini)**, **PostgreSQL**, **ChromaDB**, and **React 19 + Vite**. Featuring a graceful **interactive glowing 3D-styled orb**, **real-time token streaming (SSE)**, **speech recognition (voice input)**, **voice response synthesis (TTS)**, and a **rich in-stock inventory & order tracking catalog**.

---

## ✨ Features

- 🔮 **Graceful Glowing Orb (3D-Styled Voice UI)**: An animated spherical centerpiece that dynamically transitions between visual states:
  - **Idle**: Gentle breathing and ambient glowing pulse.
  - **Listening**: Audio reactive ripples responding to voice input.
  - **Thinking**: Chromatic gradient vortex while searching live inventory.
  - **Speaking / Streaming**: Audio equalizer waveform visualizer during responses.
- 🎙️ **Voice & Speech Recognition**: Native Web Speech API integration for instant voice queries. Tap the orb or mic button to talk naturally.
- 🔊 **Voice Speech Synthesis (TTS)**: Optional speech playback that reads the assistant's responses aloud.
- ⚡ **Real-Time Token Streaming**: Server-Sent Events (SSE) stream tokens with typewriter precision.
- 📦 **Rich In-Stock Catalog**: 23+ pre-populated products across 8 categories (Electronics, Audio, Wearables, Footwear, Fashion, Home & Kitchen, Bags, Personal Care) with guaranteed in-stock availability (15–95 units each).
- 🚚 **Order Tracking**: Live order status lookup for orders (#1001 to #1005) with courier tracking numbers and estimated delivery dates.
- 🛡️ **Zero-Friction Database Resilience**: Auto-seeds PostgreSQL on startup and seamlessly falls back to local SQLite if PostgreSQL is offline.
- 🔐 **JWT Authentication & Demo Access**: Secure OAuth2 password flow with 1-Click Instant Demo Login.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **AI / LLM**: LangChain Google GenAI (`gemini-2.5-flash`)
- **Vector DB**: ChromaDB (`models/text-embedding-004`)
- **Relational DB**: PostgreSQL via SQLAlchemy 2.0 (with SQLite fallback)
- **Document DB**: Motor / MongoDB (with in-memory cache fallback)
- **Auth**: JWT (python-jose, passlib, bcrypt)

### Frontend
- **Framework**: React 19 + Vite
- **Styling**: Tailwind CSS + Glassmorphism Custom Animations
- **Routing**: React Router DOM v7
- **APIs**: Fetch ReadableStream (SSE) & Axios
- **Speech**: Web Speech API (`SpeechRecognition` & `SpeechSynthesis`)

---

## 📂 Project Structure

```
ecommerce-ai-assistant/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py              # Login & JWT token endpoints
│   │       ├── chat.py              # Standard & SSE streaming chat endpoints
│   │       └── dependencies.py      # Auth dependency injection
│   ├── core/
│   │   ├── config.py            # Pydantic environment configuration
│   │   └── security.py          # Password hashing & JWT helpers
│   ├── database/
│   │   ├── catalog_data.py      # 23 rich products & 5 sample orders
│   │   ├── chromadb.py          # ChromaDB vector store & embeddings
│   │   ├── mongodb.py           # MongoDB async client
│   │   └── postgres.py          # SQLAlchemy engine & auto-seeding
│   ├── models/
│   │   ├── domain/
│   │   │   └── postgres_models.py # ProductDB & OrderDB schemas
│   │   └── schemas/
│   │       └── pydantic_schemas.py # Request/Response schemas
│   ├── services/
│   │   ├── ai/
│   │   │   ├── agents.py        # AIAssistant with streaming & tool execution
│   │   │   ├── memory.py        # Chat history persistence
│   │   │   ├── prompts.py       # Conversational system prompt
│   │   │   └── tools/
│   │   │       └── store_tools.py # Search, Track, Categories & Vector tools
│   │   └── db_service.py        # Database query operations
│   └── main.py                  # FastAPI entrypoint & lifespan manager
├── frontend-react/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Chat.jsx         # Glowing Orb voice & streaming chat interface
│   │   │   └── Login.jsx        # Glassmorphic login with 1-click demo access
│   │   ├── services/
│   │   │   └── api.js           # REST & SSE stream API client
│   │   ├── App.css              # Custom keyframes for glowing orb & waveforms
│   │   ├── App.jsx              # Application router
│   │   └── main.jsx             # React root
│   ├── package.json
│   └── vite.config.js
├── .env                         # Server & AI configurations
├── requirements.txt             # Python backend dependencies
└── seed_vector.py               # Standalone vector store seed utility
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.14 supported)
- Node.js 18+ and npm
- (Optional) PostgreSQL & MongoDB instances (app automatically uses SQLite/in-memory if offline)

---

### 2. Environment Configuration

Create or verify the `.env` file in the root directory:

```env
# Server Settings
APP_NAME="E-commerce AI Assistant"
DEBUG=True

# Security Settings
SECRET_KEY="super-secret-jwt-token-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_ai
MONGODB_URL="mongodb://localhost:27017"
MONGODB_DB_NAME="ecommerce_chat"

# AI Model Configuration
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
model="gemini-2.5-flash"
```

---

### 3. Backend Setup

1. **Activate Virtual Environment & Install Dependencies**:
   ```powershell
   # Windows PowerShell
   cd e:\ecommerce-ai-assistant
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start the FastAPI Server**:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
   *The database is automatically seeded with 23 in-stock products and 5 orders on startup.*

3. Verify Backend Health:
   - Root: `http://localhost:8000/`
   - AI Health: `http://localhost:8000/health/ai`
   - Swagger Docs: `http://localhost:8000/docs`

---

### 4. Frontend Setup

1. **Install Dependencies & Start Development Server**:
   ```powershell
   cd e:\ecommerce-ai-assistant\frontend-react
   npm install
   npm run dev
   ```

2. **Open the App**:
   - Navigate to `http://localhost:5173` in Google Chrome or Microsoft Edge.
   - Click **⚡ 1-Click Instant Demo Login** (or use `testuser` / `password123`).

---

## 💬 Try These Voice / Text Queries

| Purpose | Example Query |
| :--- | :--- |
| **Search Products** | *"Show me wireless earbuds in stock"* |
| **Browse Shoes** | *"Do you have running shoes or hiking boots?"* |
| **Track Orders** | *"Where is my order #1001?"* or *"Track order 1002"* |
| **Product Specs** | *"Tell me about the BaristaPro Espresso Coffee Machine"* |
| **Store Categories** | *"What categories and products do you sell?"* |
| **Recommendations** | *"Recommend something for gym workouts and fitness"* |

---

## 📡 API Reference

### Authentication
- `POST /api/v1/auth/login`: Form data (`username`, `password`) returning `{ "access_token": "...", "token_type": "bearer" }`

### AI Chatbot
- `POST /api/v1/chat`: JSON payload `{"message": "..."}` returning complete JSON response.
- `POST /api/v1/chat/stream`: Real-time Server-Sent Events (SSE) stream emitting `data: {"token": "..."}` and `data: {"done": true}`.

---

## 👥 Demo Credentials
- **Username**: `testuser`
- **Password**: `password123`
