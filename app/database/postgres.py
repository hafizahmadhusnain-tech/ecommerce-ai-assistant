import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

def is_pg_reachable(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def init_db_engine():
    """Initializes PostgreSQL engine if reachable, otherwise uses local SQLite fallback"""
    if is_pg_reachable(settings.POSTGRES_HOST, settings.POSTGRES_PORT, timeout=0.5):
        try:
            eng = create_engine(settings.DATABASE_URL, echo=False)
            with eng.connect():
                pass
            print("[Database] Successfully connected to PostgreSQL.")
            return eng
        except Exception as e:
            print(f"[Database Notice] PostgreSQL auth error ({str(e)}). Using local SQLite database.")
    else:
        print("[Database Notice] PostgreSQL host is offline. Using local SQLite fallback database.")
        
    sqlite_path = os.path.join(os.getcwd(), "ecommerce_store.db")
    return create_engine(f"sqlite:///{sqlite_path}", echo=False)

engine = init_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI Dependency: Route handlers me database session inject karne ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_initial_data():
    """Auto-seeds Postgres/SQLite with rich products and sample orders if table is empty"""
    from app.models.domain.postgres_models import ProductDB, OrderDB
    from app.database.catalog_data import CATALOG_PRODUCTS, SAMPLE_ORDERS
    
    db = SessionLocal()
    try:
        count = db.query(ProductDB).count()
        if count == 0:
            for p in CATALOG_PRODUCTS:
                prod = ProductDB(
                    id=p["id"],
                    name=p["name"],
                    category=p["category"],
                    price=p["price"],
                    stock=p["stock"],
                    rating=p["rating"],
                    description=p["description"]
                )
                db.add(prod)
            db.commit()
            print(f"[Database] Successfully populated {len(CATALOG_PRODUCTS)} products in database!", flush=True)

        ord_count = db.query(OrderDB).count()
        if ord_count == 0:
            for o in SAMPLE_ORDERS:
                ord_entry = OrderDB(
                    id=o["id"],
                    customer_id=o["customer_id"],
                    status=o["status"],
                    total_amount=o["total_amount"],
                    items_summary=o["items_summary"],
                    courier=o["courier"],
                    estimated_delivery=o["estimated_delivery"]
                )
                db.add(ord_entry)
            db.commit()
            print(f"[Database] Successfully populated {len(SAMPLE_ORDERS)} sample orders in database!", flush=True)
    except Exception as e:
        db.rollback()
        print(f"[Database Seed Notice] {str(e)}", flush=True)
    finally:
        db.close()