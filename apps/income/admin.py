from django.contrib import admin
from .models import Project, ProjectCollections, ProjectService

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    
class ProjectCollectionsAdmin(admin.ModelAdmin):
    model = ProjectCollections
    
class ProjectServiceAdmin(admin.ModelAdmin):
    model = ProjectService


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectService, ProjectServiceAdmin)
admin.site.register(ProjectCollections, ProjectCollectionsAdmin)