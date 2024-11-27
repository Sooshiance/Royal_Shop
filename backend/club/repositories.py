from rest_framework.exceptions import ValidationError

from .models import Rate, Comment, Product


class RateRepository:
    @staticmethod
    def get_rates_of_product(product:Product):
        try:
            return Rate.objects.filter(product=product).filter(admin_approval=True)
        except:
            raise ValidationError("no product found!")


class CommentRepository:
    @staticmethod
    def create_comment(data):
        return Comment.objects.create(**data)

    @staticmethod
    def get_all_comments():
        return Comment.objects.all().filter(admin_approval=True)
