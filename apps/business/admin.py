from django.contrib import admin
from .models import Business

# Register your models here.
class BusinessAdmin(admin.ModelAdmin):
    model = Business


admin.site.register(Business, BusinessAdmin)