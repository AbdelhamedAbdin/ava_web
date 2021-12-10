from django.contrib import admin
from .models import ProjectsIncomeDash, ServiceIncomeDash, ExpenseDash, ExpenseIncomeDash, CashFlowDash

# Register your models here.
class ProjectsIncomeDashAdmin(admin.ModelAdmin):
    model = ProjectsIncomeDash
    
class ServiceIncomeDashAdmin(admin.ModelAdmin):
    model = ServiceIncomeDash
    
class ExpenseDashAdmin(admin.ModelAdmin):
    model = ExpenseDash
    
class ExpenseIncomeDashAdmin(admin.ModelAdmin):
    model = ExpenseIncomeDash
    
class CashFlowDashAdmin(admin.ModelAdmin):
    model = CashFlowDash


admin.site.register(ProjectsIncomeDash, ProjectsIncomeDashAdmin)
admin.site.register(ServiceIncomeDash, ServiceIncomeDashAdmin)
admin.site.register(ExpenseDash, ExpenseDashAdmin)
admin.site.register(ExpenseIncomeDash, ExpenseIncomeDashAdmin)
admin.site.register(CashFlowDash, CashFlowDashAdmin)