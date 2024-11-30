from django.db.models import Prefetch

from .models import RoyalTransactions, History
from store.services import ProductService


class HistoryRepository:
    @staticmethod
    def payment_cart_quantity(user_id):
        history_records = History.objects.filter(user_id=user_id).select_related(
        'payment__order__cart',
        'payment__order__cart__product'
        )
        for record in history_records:
            cart = record.payment.order.order.cart
            print(f"Product: {cart.product.product_title}, Quantity: {cart.quantity}")
            ProductService.update_product(cart.product.pk, cart.product.stock_qty - cart.quantity)
