from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.conf import settings
import random
from django.db.models.signals import post_save

## App Imports ##
from .utils import generate_hex_16_key


# Create your models here.
def ProfileImage_Upload(instance, filename):
    imagename, extension = filename.split(".")
    return "User/Images/%s/%s/%s.%s" % (instance.email, instance.id, imagename, extension)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, first_name, last_name, verified=False, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise serializers.ValidationError({'email': ['Email Must Be Set']},code='invalid')
        if not first_name:
            raise serializers.ValidationError({'first_name': ['First Name Must Be Set']},code='invalid')
        if not last_name:
            raise serializers.ValidationError({'last_name': ['Last Name Must Be Set']},code='invalid')
        if not password:
            raise serializers.ValidationError({'password': ['Password Must Be Set']},code='invalid')
        
        user = self.model(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, verified=True, **extra_fields):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        email = self.normalize_email(email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    first_name = models.CharField(verbose_name='First Name', null=True, blank=True, max_length=100)
    last_name = models.CharField(verbose_name='Last Name', null=True, blank=True, max_length=100)
    email = models.EmailField(
        verbose_name=_("Email address"), unique=True,error_messages={
            'unique': _(
                "A user is already registered with this email address"),
        },)
    username = models.CharField(unique=True, max_length=100, null=True, blank=True)
    
    profile_picture = models.ImageField(upload_to=ProfileImage_Upload, blank=True, null=True, default='/User/Images/default-logo.png', max_length=400) #CONFIGURE DEFAULT image
    country = models.CharField(max_length=30, blank=False, default='Egypt')
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    
    verified = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return str(self.email)
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        email = self.email.split('@')
        username = email[0]
        self.username = username
        if not self.profile_picture:
            self.profile_picture = 'images/default-logo.jpg'
        super().save(*args, **kwargs)


class VerificationKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.IntegerField(max_length=4, default=1234)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)

    def __str__(self):
        return str(self.user) + ":" + str(self.code)


def pre_save_txt_msg_code(instance, sender, *args, **kwargs):
    if kwargs['created']:
        digits = '0123456789'
        result = ''
        for i in range(0, 4):
            result += random.choice(digits)
        text_code = VerificationKey(user=instance)
        text_code.code = result
        text_code.save()


post_save.connect(receiver=pre_save_txt_msg_code, sender=User)


class ResetPasswordKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    key = models.CharField(max_length=16, default=generate_hex_16_key, unique=True)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)


class ContactSupport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=400)

    def __str__(self):
        return "user: %s, name: %s" % (self.user, self.name)
