from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import User, Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user=instance
        new_profile = Profile.objects.create(
            user=user,
            username= user.username,
        )


@receiver(pre_save, sender=Profile)
def update_user(sender, instance, **kwargs):
    if instance.pk:
        user = instance.user
        user.username = instance.username
        user.save()


def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(create_profile, sender=User)


post_delete.connect(delete_user, sender=Profile)
