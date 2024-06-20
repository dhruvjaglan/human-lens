from django.contrib import admin

from verifier.models import CustomUser, TaskObject, Company, VerificationTaskResult

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskObject)
class TaskObjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(VerificationTaskResult)
class VerificationTaskResultAdmin(admin.ModelAdmin):
    pass
