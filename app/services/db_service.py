from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.domain.postgres_models import ProductDB, OrderDB

def fetch_products(db: Session, query: str = "", category: str = "", limit: int = 8):
    """
    Searches products across name, description, and category.
    If query is generic (empty, 'all', 'products', 'browse'), returns top available in-stock items.
    """
    db_query = db.query(ProductDB)
    
    clean_q = (query or "").strip().lower()
    generic_keywords = ["", "all", "products", "items", "browse", "stock", "what do you have", "everything", "shop"]
    
    if clean_q not in generic_keywords:
        # Split terms for multi-word fuzzy matching
        terms = clean_q.split()
        filters = []
        for t in terms:
            term_filter = or_(
                ProductDB.name.ilike(f"%{t}%"),
                ProductDB.description.ilike(f"%{t}%"),
                ProductDB.category.ilike(f"%{t}%")
            )
            filters.append(term_filter)
        db_query = db_query.filter(or_(*filters))
        
    if category:
        db_query = db_query.filter(ProductDB.category.ilike(f"%{category}%"))
        
    return db_query.limit(limit).all()

def fetch_product_by_name(db: Session, name: str):
    """Legacy helper maintained for backward compatibility"""
    return fetch_products(db, query=name)

def fetch_product_by_id_or_name(db: Session, identifier: str):
    if identifier.isdigit():
        prod = db.query(ProductDB).filter(ProductDB.id == int(identifier)).first()
        if prod:
            return prod
    return db.query(ProductDB).filter(ProductDB.name.ilike(f"%{identifier}%")).first()

def fetch_order_status(db: Session, order_id: int):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if order:
        return (
            f"📦 **Order #{order.id} Tracking Details**:\n"
            f"- **Status**: `{order.status}`\n"
            f"- **Items**: {order.items_summary or 'Standard Store Items'}\n"
            f"- **Courier & Tracking**: {order.courier}\n"
            f"- **Estimated Delivery**: {order.estimated_delivery}\n"
            f"- **Total Amount**: Rs. {order.total_amount:,.2f}"
        )
    return f"Maaf kijiye, Order #{order_id} hamare system me nahi mila. Barah-e-karam apna Order ID dobara check karein (jaise #1001, #1002, #1003)."

def fetch_categories_and_promos(db: Session):
    products = db.query(ProductDB).all()
    categories = sorted(list(set(p.category for p in products if p.category)))
    total_stock = sum(p.stock for p in products)
    return {
        "categories": categories,
        "total_products": len(products),
        "total_units_in_stock": total_stock
    }