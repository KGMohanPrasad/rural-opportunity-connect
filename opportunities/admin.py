from django.contrib import admin
from .models import Job, SavedOpportunity

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'location', 'salary_min', 'salary_max', 'deadline')
    list_filter = ('location', 'job_type', 'deadline')
    search_fields = ('title', 'organization')

@admin.register(SavedOpportunity)
class SavedOpportunityAdmin(admin.ModelAdmin):
    list_display = ('user', 'opportunity_type', 'opportunity_id', 'saved_at')
    list_filter = ('opportunity_type', 'saved_at')
