from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    EDUCATION_CHOICES = [
        ('10th', '10th Pass'),
        ('12th', '12th Pass'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('diploma', 'Diploma'),
        ('other', 'Other'),
    ]
    
    INTEREST_CHOICES = [
        ('jobs', 'Jobs & Employment'),
        ('scholarships', 'Scholarships'),
        ('schemes', 'Government Schemes'),
        ('skills', 'Skill Development'),
        ('business', 'Business Opportunities'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    course = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    experience = models.TextField(blank=True, help_text="Work experience details")
    annual_income = models.CharField(max_length=50, blank=True)
    interests = models.CharField(max_length=100, blank=True, help_text="Comma-separated interests")
    preferred_opportunity = models.CharField(max_length=50, choices=INTEREST_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}" or self.user.username

    def profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [
            self.age,
            self.location,
            self.education,
            self.course,
            self.skills,
            self.experience,
            self.annual_income,
            self.interests,
            self.preferred_opportunity
        ]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)
