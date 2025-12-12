from pydantic import BaseModel
from beanie import Document


class Product(Document):
    name:str
    description:str
    quantity:int
    price:float

    class Settings:
        name = "products"