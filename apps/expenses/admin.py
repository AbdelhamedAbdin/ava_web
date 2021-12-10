from django.contrib import admin
from .models import ExpenseCategory, Payment, PaymentSummary

class ExpenseCategoryAdmin(admin.ModelAdmin):
    model = ExpenseCategory

class PaymentAdmin(admin.ModelAdmin):
    model = Payment

class PaymentSummaryAdmin(admin.ModelAdmin):
    model = PaymentSummary

admin.site.register(PaymentSummary, PaymentSummaryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)