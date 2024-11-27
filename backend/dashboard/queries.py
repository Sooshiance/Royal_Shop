from django.db.models import Q, F, Avg, Subquery, OuterRef

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


class UserQuery:
    @staticmethod
    def user_with_phone():
        pass

    @staticmethod
    def user_with_email():
        pass


class RateQuery:
    @staticmethod
    def highest_average_rate_products():
        rates = Rate.objects.filter(product=OuterRef('pk')).values('product')
        average_rating = rates.annotate(avg_vote=Avg('vote')).values('avg_vote')
        return Product.objects.annotate(
        average_rating=Subquery(average_rating)
        ).order_by('-average_rating')
