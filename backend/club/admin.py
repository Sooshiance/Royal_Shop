from django.contrib import admin

from .models import Rate, Comment


class RateAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'product', 'each_product_rate']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['status']


admin.site.register(Rate, RateAdmin)

admin.site.register(Comment, CommentAdmin)
