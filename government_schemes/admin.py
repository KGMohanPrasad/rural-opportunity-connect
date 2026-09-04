from django.contrib import admin
from .models import GovernmentScheme

@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'category')
    list_filter = ('category', 'department')
    search_fields = ('name', 'department')
