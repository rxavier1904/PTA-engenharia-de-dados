from pydantic import BaseModel
from typing import Optional

class ItemPedidoRaw(BaseModel):
    order_id: str
    order_item_id: int
    product_id: str
    seller_id: str
    shipping_limit_date: str
    price: Optional[float] = None #aceita o none pra testar a logica da mediana
    freight_value: Optional[float] = None
