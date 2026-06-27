from ..session import get_session
from ..models import Order, OrderItem

class OrdersRepository:
    def create(self, ref, total, currency, recipient, delivery, sender, gift_message, expires_at, cart):
        with get_session() as session:
            session.add(Order(id=ref, total_amount=total, currency=currency, recipient=recipient,
                               delivery=delivery, sender=sender, gift_message=gift_message,
                               expires_at=expires_at))
            session.flush()  # order_items has no ORM relationship() to infer insert order from
            for item in cart:
                session.add(OrderItem(order_id=ref, product_id=item["product_id"],
                                       quantity=item["quantity"], icing_text=item.get("icing_text")))

    def get(self, order_id):
        with get_session() as session:
            order = session.get(Order, order_id)
            if not order:
                return None
            return {"id": order.id, "status": order.status, "total_amount": float(order.total_amount),
                    "currency": order.currency, "created_at": order.created_at}