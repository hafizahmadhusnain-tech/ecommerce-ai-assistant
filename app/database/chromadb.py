from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
import os

# ChromaDB ka local storage folder define karna
CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")

def get_embedding_function():
    try:
        # Standard Google GenAI text embedding model
        return GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=settings.GEMINI_API_KEY
        )
    except Exception:
        try:
            return GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-2", 
                google_api_key=settings.GEMINI_API_KEY
            )
        except Exception:
            return None

_vector_store = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        try:
            emb = get_embedding_function()
            if emb:
                _vector_store = Chroma(
                    persist_directory=CHROMA_PATH,
                    embedding_function=emb,
                    collection_name="products_vector_store"
                )
        except Exception as e:
            print(f"[ChromaDB Init Warning] {str(e)}")
    return _vector_store

def add_products_to_vector_db(products_list: list):
    """
    Products ko Vector DB me save karne ka function.
    Format of products_list: [{"id": "1", "text": "Product Name & Description", "metadata": {...}}]
    """
    vs = get_vector_store()
    if vs is None:
        print("[ChromaDB] Vector store not initialized.")
        return
    texts = [p["text"] for p in products_list]
    metadatas = [p["metadata"] for p in products_list]
    ids = [str(p["id"]) for p in products_list]
    
    vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    print(f"Successfully added {len(texts)} products to ChromaDB Vector Store!")

def seed_vector_store_if_needed():
    """Auto-seeds ChromaDB with the full product catalog if collection is empty"""
    vs = get_vector_store()
    if vs is None:
        return
    try:
        from app.database.catalog_data import CATALOG_PRODUCTS
        # Check if vector store already has data
        existing = vs.get(limit=1)
        if not existing or len(existing.get("ids", [])) == 0:
            print("[ChromaDB] Seeding full product catalog into ChromaDB...")
            formatted_products = [
                {
                    "id": p["id"],
                    "text": f"{p['name']} - Category: {p['category']} | Price: Rs.{p['price']} | In Stock: {p['stock']} units | Rating: {p['rating']} stars. {p['description']}",
                    "metadata": {"category": p["category"], "price": p["price"], "stock": p["stock"]}
                }
                for p in CATALOG_PRODUCTS
            ]
            add_products_to_vector_db(formatted_products)
    except Exception as e:
        print(f"[ChromaDB Seed Warning] {str(e)}")