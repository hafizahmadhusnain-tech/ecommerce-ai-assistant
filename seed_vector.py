import os
import sys

# Current folder ko path me add karna taake imports chal sakein
sys.path.append(os.getcwd())

from app.database.chromadb import add_products_to_vector_db
from app.database.catalog_data import CATALOG_PRODUCTS

if __name__ == "__main__":
    print(f"Injecting {len(CATALOG_PRODUCTS)} catalog products into Vector Database...")
    formatted_products = [
        {
            "id": p["id"],
            "text": f"{p['name']} - Category: {p['category']} | Price: Rs.{p['price']} | In Stock: {p['stock']} units | Rating: {p['rating']} stars. {p['description']}",
            "metadata": {"category": p["category"], "price": p["price"], "stock": p["stock"]}
        }
        for p in CATALOG_PRODUCTS
    ]
    add_products_to_vector_db(formatted_products)
    print("Done! Vector database successfully seeded with complete catalog.")