from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'location', 'education', 'course', 'completion_score', 'preferred_opportunity', 'updated_at')
    list_filter = ('education', 'preferred_opportunity', 'location')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'location', 'skills')
    ordering = ('-updated_at',)

    @admin.display(description='Username')
    def user_username(self, obj):
        return obj.user.username

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description='Profile Strength')
    def completion_score(self, obj):
        return f"{obj.profile_completion_percentage()}%"
