from django.db import models

class GovernmentScheme(models.Model):
    CATEGORY_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('education', 'Education'),
        ('employment', 'Employment'),
        ('housing', 'Housing'),
        ('financial', 'Financial Assistance'),
        ('healthcare', 'Healthcare'),
        ('skills', 'Skill Development'),
        ('women', 'Women & Children'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('rural', 'Rural Development'),
    ]

    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    target_beneficiaries = models.TextField()
    benefits = models.TextField()
    eligibility = models.TextField()
    required_documents = models.TextField()
    application_process = models.TextField()
    official_website = models.URLField(blank=True)
    source_portal = models.CharField(max_length=100, default='myScheme.gov.in', blank=True)
    source_url = models.URLField(blank=True, default='https://www.myscheme.gov.in/')
    is_external = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
