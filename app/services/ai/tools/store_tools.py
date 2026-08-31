import re
from langchain_core.tools import tool
from app.database.postgres import SessionLocal
from app.services.db_service import (
    fetch_products, 
    fetch_order_status, 
    fetch_categories_and_promos,
    fetch_product_by_id_or_name
)
from app.database.chromadb import get_vector_store

@tool
def search_products(query: str = "") -> str:
    """
    Search store products by name, keyword, category, or description.
    Use this tool whenever the customer asks about products, wants to browse what's in stock, or searches for specific items (e.g. 'shoes', 'headphones', 'coffee', 'watches', 'all items').
    """
    db = SessionLocal()
    try:
        products = fetch_products(db, query=query)
        if not products:
            # Fallback to general products
            products = fetch_products(db, query="", limit=5)
            if not products:
                return "Store catalog is currently getting updated. Please check back in a moment."
            result = f"We couldn't find exact matches for '{query}', but here are our top featured items currently in stock:\n"
        else:
            result = "Here are the matching products currently available in stock:\n"
            
        for p in products:
            result += (
                f"- **{p.name}** | Price: Rs. {p.price:,.0f} | Stock: {p.stock} units available | Rating: {p.rating}/5.0\n"
                f"  Category: {p.category}\n"
                f"  Description: {p.description}\n"
            )
        return result
    except Exception as e:
        return f"Error while retrieving products: {str(e)}"
    finally:
        db.close()

@tool
def track_order(order_id: str) -> str:
    """
    Track order status, delivery date, courier and items using the Order ID (e.g. 1001, #1002, 1003).
    Use this tool whenever the customer asks about order status or delivery updates.
    """
    db = SessionLocal()
    try:
        # Extract digits from input (e.g. "#1001" -> 1001)
        digits = re.findall(r'\d+', str(order_id))
        if not digits:
            return "Please provide a valid Order ID number (for example, #1001, #1002, or #1003)."
        clean_id = int(digits[0])
        return fetch_order_status(db, clean_id)
    except Exception as e:
        return f"Error looking up order: {str(e)}"
    finally:
        db.close()

@tool
def list_store_categories() -> str:
    """
    Get an overview of all available product categories and total inventory in stock.
    Use this tool when the customer asks what categories we have, what we sell, or general store info.
    """
    db = SessionLocal()
    try:
        data = fetch_categories_and_promos(db)
        cats = ", ".join(data["categories"])
        return (
            f"🛒 **Store Overview**:\n"
            f"- Available Categories: {cats}\n"
            f"- Active In-Stock Products: {data['total_products']} items ({data['total_units_in_stock']} total units in stock ready to ship)\n"
            f"- Special Offer: Free Express Shipping on orders over Rs. 3,000!"
        )
    except Exception as e:
        return f"Error retrieving store categories: {str(e)}"
    finally:
        db.close()

@tool
def semantic_product_recommendation(user_query: str) -> str:
    """
    Semantic search to find products matching user benefits, use-case, lifestyle, or vibe (e.g. 'gifts for developer', 'gym workouts', 'studying at night').
    """
    try:
        vs = get_vector_store()
        if vs:
            docs = vs.similarity_search(user_query, k=3)
            if docs:
                result = "Based on your requirements, here are the best recommendations:\n"
                for doc in docs:
                    result += f"- {doc.page_content}\n"
                return result
    except Exception:
        pass
    
    # Fallback to postgres search
    db = SessionLocal()
    try:
        products = fetch_products(db, query=user_query, limit=3)
        if products:
            result = "Here are recommended in-stock items matching your request:\n"
            for p in products:
                result += f"- **{p.name}** (Rs. {p.price:,.0f}) - {p.description} (Stock: {p.stock} units)\n"
            return result
        return "We have lots of exciting products! Ask me about headphones, smartwatches, running shoes, hoodies, coffee machines, and more."
    finally:
        db.close()        