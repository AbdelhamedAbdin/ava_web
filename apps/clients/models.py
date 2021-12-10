from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(verbose_name="Client Name", max_length=80, blank=True, null=True)
    company_name = models.CharField(verbose_name="Company Name", max_length=80, blank=True, null=True)
    email = models.EmailField(verbose_name="Email", max_length=80, blank=True, null=True)
    phone = models.CharField(verbose_name="Phone Number", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created Date", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated Date", auto_now=True)
    
    def __str__(self):
        return str(self.client_name)
