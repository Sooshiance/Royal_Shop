from django.db import models

from .enums import PaymentStatus

from user.models import User
from store.models import OrderItem


class RoyalTransactions(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='royal_user')
    order          = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=256)
    tax            = models.DecimalField(max_digits=12, decimal_places=0)
    authorized_key = models.CharField(max_length=48)
    card_hash      = models.CharField(null=True, blank=True, max_length=512, default=None)
    status         = models.PositiveSmallIntegerField(choices=PaymentStatus.choices(), default=1)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def payment_failure(self):
        self.status = PaymentStatus.Failed
        self.save()


class History(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_history')
    payment = models.ForeignKey(RoyalTransactions, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} {self.payment.order}'
