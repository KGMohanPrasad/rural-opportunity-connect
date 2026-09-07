from django.db import models
from accounts.models import UserProfile

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    required_skills = models.TextField(help_text="Comma-separated skills")
    experience_required = models.CharField(max_length=100)
    deadline = models.DateField()
    source_portal = models.CharField(max_length=100, default='National Career Service', blank=True)
    source_url = models.URLField(blank=True, default='https://www.ncs.gov.in/')
    is_external = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def skills_list(self):
        if not self.required_skills:
            return []
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    def __str__(self):
        return f"{self.title} - {self.organization}"


class SavedOpportunity(models.Model):
    OPPORTUNITY_TYPE = [
        ('job', 'Job'),
        ('scholarship', 'Scholarship'),
        ('scheme', 'Government Scheme'),
        ('skill', 'Skill Program'),
        ('business', 'Business Opportunity'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='saved_opportunities')
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE)
    opportunity_id = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.opportunity_type} {self.opportunity_id}"
