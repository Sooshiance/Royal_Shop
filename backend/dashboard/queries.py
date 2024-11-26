from django.db.models import Q, F, Avg

from rest_framework.exceptions import ValidationError

from store.models import Product
from user.models import User
from club.models import Rate


class ProductQuery:
    @staticmethod
    def all_in_stock_product(status):
        if status == "full":
            return Product.objects.filter(in_stock=True)
        if status == "empty":
            return Product.objects.filter(in_stock=False)
        else:
            raise ValidationError(detail="Not an option!")

    @staticmethod
    def stock_qty_product(threshold_qty, status):
        if status == "lower":
            return Product.objects.filter(stock_qty__lt=threshold_qty)
        if status == "higher":
            return Product.objects.filter(stock_qty__gte=threshold_qty)
        else:
            raise ValidationError(detail="Not an option!")
    
    @staticmethod
    def highest_average_rate_products():
        return Product.objects.annotate(
            average_rating=Avg('rate_product__vote')
        ).order_by('-average_rating')


class UserQuery:
    pass


class RateQuery:
    pass
