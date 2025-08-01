from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("products.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
conn.commit()

class Product(BaseModel):
    name: str
    price: float

@app.post("/products")
def create_product(product: Product):
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product.name, product.price))
    conn.commit()
    return {"message": "Product added successfully"}

@app.get("/products")
def get_products():
    cursor.execute("SELECT * FROM products")
    return [{"id": row[0], "name": row[1], "price": row[2]} for row in cursor.fetchall()]
