from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")

USER_SERVICE_URL = "http://localhost:8000"
PRODUCT_SERVICE_URL = "http://localhost:8001"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request):
    users = requests.get(f"{USER_SERVICE_URL}/users").json()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/users")
def add_user(name: str = Form(...), email: str = Form(...)):
    requests.post(f"{USER_SERVICE_URL}/users", json={"name": name, "email": email})
    return {"message": "User created"}

@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request):
    products = requests.get(f"{PRODUCT_SERVICE_URL}/products").json()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.post("/products")
def add_product(name: str = Form(...), price: float = Form(...)):
    requests.post(f"{PRODUCT_SERVICE_URL}/products", json={"name": name, "price": price})
    return {"message": "Product created"}
