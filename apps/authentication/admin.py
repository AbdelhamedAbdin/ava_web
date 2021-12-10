from django.contrib import admin

from django.contrib.auth import get_user_model
from .models import ContactSupport
User = get_user_model()

# Register your models here.
class AppUserAdmin(admin.ModelAdmin):
    model = User
    readonly_fields = ('id',)


admin.site.register(User, AppUserAdmin)
admin.site.register(ContactSupport)
