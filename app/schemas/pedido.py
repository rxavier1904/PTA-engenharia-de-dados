from pydantic import BaseModel
from typing import Optional


from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel
from typing import Optional, Any

class PedidoInput(BaseModel):
    order_id: Optional[Any] = None
    customer_id: Optional[Any] = None
    order_status: Optional[Any] = None
    order_purchase_timestamp: Optional[Any] = None
    order_approved_at: Optional[Any] = None
    order_delivered_carrier_date: Optional[Any] = None
    order_delivered_customer_date: Optional[Any] = None
    order_estimated_delivery_date: Optional[Any] = None
    tempo_entrega_dias: Optional[Any] = None
    tempo_entrega_estimado_dias: Optional[Any] = None
    entrega_no_prazo: Optional[Any] = None
    message: Optional[Any] = None
    total_registros: Optional[Any] = None
    dados: Optional[Any] = None


    class Config:
        extra = "ignore"  




class PedidoProcessado(BaseModel):
    """Schema para dados de pedidos após processamento."""
    order_id: Optional[str] = None
    order_status: Optional[str] = None
    order_purchase_timestamp: Optional[str] = None
    order_approved_at: Optional[str] = None
    order_delivered_carrier_date: Optional[str] = None
    order_delivered_customer_date: Optional[str] = None
    order_estimated_delivery_date: Optional[str] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = None
