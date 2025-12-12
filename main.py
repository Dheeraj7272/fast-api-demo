from fastapi import FastAPI,HTTPException
from models import Product
from config.db import init_db
from beanie import PydanticObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3001",   # your frontend local dev
    "http://127.0.0.1:3001",
    # "http://your-domain.com",  # add production domain here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, DELETE
    allow_headers=["*"],          # Authorization, Content-Type, etc.
)
@app.on_event("startup")
async def start_db():
     await init_db()

@app.get("/")
def greet():
    return "Welcome to my first fast api backend"

@app.get("/products")
async def get_all_products():
   return await Product.find_all().to_list()

greet()  

@app.get("/product/{id}",response_model=Product)
async def get_product_by_id(id:PydanticObjectId):
    product = await Product.get(id)    
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    return product

@app.post("/products")
async def create_product_by_id(product: Product):
    await product.insert()
    return product

@app.put("/product/{product_id}",response_model=Product)
async def update_product_information(product_id:PydanticObjectId,data:Product):
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    update_data = data.dict(exclude_unset=True)
    await product.set(update_data)
    return product

@app.delete("/product/{id}")
async def delete_product_by_id(id:PydanticObjectId):
    product = await Product.get(id)    
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    await product.delete()
    return {"message":"Product delted successfully"}
