from pydantic import BaseModel, field_validator
from typing import Optional

class ProdutoRaw(BaseModel):
    product_id: str
    product_category_name: str
    product_name_lenght: Optional[float] = None
    product_description_lenght: Optional[float] = None
    product_photos_qty: Optional[float] = None
    product_weight_g: Optional[float] = None
    product_length_cm: Optional[float] = None
    product_height_cm: Optional[float] = None
    product_width_cm: Optional[float] = None
    
    @field_validator('product_name_lenght', 'product_description_lenght', 'product_photos_qty', 
                     'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm', mode='before')
    @classmethod
    def convert_empty_to_none(cls, v):
        """Converte strings vazias para None."""
        if v == "" or v is None:
            return None
        return v

    