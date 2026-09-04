from django.contrib import admin
from .models import Scholarship

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'amount', 'education_level', 'application_deadline')
    list_filter = ('education_level', 'category', 'application_deadline')
    search_fields = ('name', 'provider')
