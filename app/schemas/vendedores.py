from pydantic import BaseModel
from typing import Optional

class VendedorRaw(BaseModel):
    seller_id: str
    seller_zip_code_prefix: Optional[int] = None
    seller_city: str
    seller_state: str
