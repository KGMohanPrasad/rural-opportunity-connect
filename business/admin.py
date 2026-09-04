from django.contrib import admin
from .models import BusinessOpportunity

@admin.register(BusinessOpportunity)
class BusinessOpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'investment_level', 'opportunity_level')
    list_filter = ('category', 'investment_level', 'opportunity_level')
    search_fields = ('name', 'category')
