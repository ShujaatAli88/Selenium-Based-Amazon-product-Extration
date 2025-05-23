from pydantic import BaseModel


class ValidateData(BaseModel):
    product_id: str
    product_name: str
    product_price: str
    product_rating: str
    image_url: str
