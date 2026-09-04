from django.contrib import admin
from .models import SkillProgram

@admin.register(SkillProgram)
class SkillProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'provider', 'level', 'price_type')
    list_filter = ('category', 'level', 'price_type')
    search_fields = ('name', 'provider', 'category')
