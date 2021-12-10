from django.db import models
from django.db.models.aggregates import Max, Sum
from django.contrib.auth import get_user_model
User = get_user_model()


# External App Imports
from apps.services.models import Service
from apps.income.models import Project , ProjectService
from apps.income.choices import StateCollectionChoices
from apps.expenses.models import Payment , ExpenseCategory
# from apps.expenses.choices import state


#1 Total Of ALL Projects (Collected | Remaining) :WHEN USER CREATED
class ProjectsIncomeDash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, related_name="projectsdash")
    total_collecetd_projects = models.DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    total_remaining_projects = models.DecimalField(max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    
    class Meta:
        verbose_name = "Projects Dashboard"
        verbose_name_plural = "Projects Dashboards"
        
    def __str__(self):
        return str(self.user)
        
    def save(self, *args, **kwargs):
        if self.user.project_set.all().exists():
            self.total_collecetd_projects = self.user.project_set.filter(total_collected__isnull = False).aggregate(Sum('total_collected'))['total_collected__sum']
            self.total_remaining_projects = self.user.project_set.filter(remaining_balance__isnull = False).aggregate(Sum('remaining_balance'))['remaining_balance__sum']
        super().save(*args, **kwargs)
        

#----------------------------------------------------------------
#3 Total Of each Service + Highest Service Income
class ServiceIncomeDash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, unique=True, related_name="servicedash")
    # highest_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="highestservicedash")
    total_for_service = models.DecimalField(max_digits=10, decimal_places=2,  blank=True, null=True)
    
    class Meta:
            verbose_name = "Service Dashboard"
            verbose_name_plural = "Services Dashboards"
    
    def __str__(self):
        return f'{self.user} | {self.service}'
            
    def save(self, *args, **kwargs):
        if self.service.project_service.exists():
            self.total_for_service = self.service.project_service.filter(total_service_price__isnull = False).aggregate(Sum('total_service_price'))['total_service_price__sum']
            # Get Highest Service Income #Working - Uncomment if needed 
            
            # highest_service = self.user.serviceincomedash_set.filter(total_for_service__isnull = False).annotate(Max('total_for_service'))[0]
            # self.highest_service = highest_service.service
            super().save(*args, **kwargs)

#----------------------------------------------------------------
#2 Total Of ALL expense categories (Paid | Remaining) :WHEN USER CREATED
class ExpenseDash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid_exp_cat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    remaining_exp_cat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
            verbose_name = "TotExpCategories Dashboard"
            verbose_name_plural = "TotExpCategories Dashboards"
    
    def __str__(self):
        return str(self.user)
            
    def save(self, *args, **kwargs):
        if ExpenseCategory.objects.filter(user=self.user).exists():
            self.paid_exp_cat = Payment.objects.filter(user=self.user).filter(paid_amount__isnull = False).aggregate(Sum('paid_amount'))['paid_amount__sum']
            self.remaining_exp_cat = Payment.objects.filter(user=self.user).filter(remaining__isnull=False).aggregate(Sum('remaining'))['remaining__sum']
            # self.paid_exp_cat = self.user.payment_set.objects.filter(paid_amount__isnull = False).aggregate(Sum('paid_amount'))['paid_amount__sum']
            # self.remaining_exp_cat = self.user.payment_set.objects.filter(remaining__isnull = False).aggregate(Sum('remaining'))['remaining__sum']
            super().save(*args, **kwargs)

#----------------------------------------------------------------
#4 Total Of each expense category + Highest expense category     
class ExpenseIncomeDash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_cat = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, unique=True, related_name="expensecat")
    total_for_category = models.DecimalField(max_digits=10, decimal_places=2,  blank=True, null=True)
    
    class Meta:
            verbose_name = "ExpCategory Dashboard"
            verbose_name_plural = "ExpCategories Dashboards"
            
    def __str__(self):
        return str(self.user)
            
    def save(self, *args, **kwargs):
        if self.user.expensecategory_set.exists():
            self.total_for_category = self.user.payment_set.objects.filter(expense_category=self.expense_cat).aggregate(Sum('paid_amount'))['paid_amount__sum']
            # Get Highest Expense Cat In View
            # self.total_for_category = Payment.objects.all(expense_categor=self.expense_cat, user=self.request.user).aggregate(Max('paid_amount'))['paid_amount__max']
            super().save(*args, **kwargs)

#----------------------------------------------------------------
#5 Weekly Collections | Payments
#6 Monthly Collections | Payments
class CashFlowDash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass

    class Meta:
            verbose_name = "CashFlow Dashboard"
            verbose_name_plural = "CashFlow Dashboards"

    def __str__(self):
        return str(self.user)
    
    



'''
class IncomeDash(models.Model):
    1# Total Of ALL Projects (Collected | Remaining)
    3# Total Of each Service + Highest Service Income
class ExpenseDash(models.Model):
    2# Total Of ALL Projects (Paid | Remaining)
    4# Total Of each expense category + Highest expense category 
class CashFlowDash(models.Model):
    5# Weekly Collections | Payments
    6# Monthly Collections | Payments
'''