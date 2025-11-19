from pydantic import BaseModel
from typing import Optional


class PedidoInput(BaseModel):
    """Schema para receber dados brutos de pedidos."""
    order_id: Optional[str] = None
    order_status: Optional[str] = None
    order_purchase_timestamp: Optional[str] = None
    order_approved_at: Optional[str] = None
    order_delivered_carrier_date: Optional[str] = None
    order_delivered_customer_date: Optional[str] = None
    order_estimated_delivery_date: Optional[str] = None


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
