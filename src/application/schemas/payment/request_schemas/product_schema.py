from pydantic import BaseModel, Field, HttpUrl


class CreateProductRequestSchema(BaseModel):
    product_name: str = Field(..., description="Product name", min_length=5, max_length=15)
    image: HttpUrl = Field(..., description="Image url")
