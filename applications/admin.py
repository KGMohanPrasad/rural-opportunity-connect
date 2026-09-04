from django.contrib import admin
from .models import Application, DocumentChecklist

@admin.action(description="Mark selected applications as 'Under Review'")
def make_under_review(modeladmin, request, queryset):
    queryset.update(status='under_review')

@admin.action(description="Mark selected applications as 'Shortlisted'")
def make_shortlisted(modeladmin, request, queryset):
    queryset.update(status='shortlisted')

@admin.action(description="Mark selected applications as 'Selected / Granted'")
def make_selected(modeladmin, request, queryset):
    queryset.update(status='selected')

@admin.action(description="Mark selected applications as 'Rejected'")
def make_rejected(modeladmin, request, queryset):
    queryset.update(status='rejected')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'opportunity_name', 'opportunity_type', 'user', 'organization', 'status', 'applied_date', 'updated_date')
    list_display_links = ('id', 'opportunity_name')
    list_editable = ('status',)
    list_filter = ('status', 'opportunity_type', 'applied_date')
    search_fields = ('opportunity_name', 'organization', 'user__user__username', 'user__user__email')
    ordering = ('-applied_date',)
    date_hierarchy = 'applied_date'
    actions = [make_under_review, make_shortlisted, make_selected, make_rejected]
    list_per_page = 25

@admin.register(DocumentChecklist)
class DocumentChecklistAdmin(admin.ModelAdmin):
    list_display = ('user', 'documents_ready_count', 'aadhaar', 'marksheet', 'income_certificate', 'community_certificate', 'updated_at')
    search_fields = ('user__user__username', 'user__user__email')
    list_filter = ('aadhaar', 'income_certificate', 'community_certificate')
