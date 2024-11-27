from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

from .enums import CommentType

from user.models import User
from store.models import Product


class Rate(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rate_profile')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rate_product')
    vote = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    txt = models.CharField(max_length=255, blank=True, null=True)
    admin_approval = models.BooleanField(default=False)
    
    def each_product_rate(self):
        return Rate.objects.filter(product=self.product).aggregate(Avg('vote'))['vote__avg']
    
    def __str__(self):
        return f"{self.user_profile.username} has this opinion about {self.product.product_title}"


class Comment(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    txt = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=CommentType.choices(), default=1)
    admin_approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_profile.username}"
