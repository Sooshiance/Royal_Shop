from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin,)

from shortuuid.django_fields import ShortUUIDField


class AllUser(BaseUserManager):
    def create_user(self, username, password=None):
        
        if not username:
            raise ValueError("Need Username")

        user = self.model(
            username=username,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = False        
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = True        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uid          = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")
    # Users can send phone or email to `username` field
    username     = models.TextField(unique=True)
    # If phone was sent, this flag will become `True`
    is_phone     = models.BooleanField(default=False)
    # If email was sent, this flag will become `True`
    is_email     = models.BooleanField(default=False)

    is_active    = models.BooleanField(default=True, null=False)
    is_staff     = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = AllUser()

    USERNAME_FIELD  = 'username'
    
    def __str__(self):
        return f"{self.username}"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username        = models.CharField(max_length=255, unique=True)
    email           = models.EmailField(unique=True, blank=True, null=True)
    phone           = models.CharField(unique=True, max_length=11, blank=True, null=True)
    first_name      = models.CharField(max_length=127, null=True, blank=True)
    last_name       = models.CharField(max_length=127, null=True, blank=True)
    bio             = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    website         = models.URLField(blank=True, null=True)
    location        = models.CharField(max_length=144, blank=True, null=True)
    birth_date      = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
