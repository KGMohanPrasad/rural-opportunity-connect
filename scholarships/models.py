from django.db import models

class Scholarship(models.Model):
    EDUCATION_LEVEL = [
        ('12th', '12th Pass'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('diploma', 'Diploma'),
    ]

    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.CharField(max_length=100)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL)
    eligibility = models.TextField()
    income_limit = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    course = models.CharField(max_length=100, blank=True)
    required_documents = models.TextField()
    application_deadline = models.DateField()
    source_portal = models.CharField(max_length=100, default='Buddy4Study', blank=True)
    source_url = models.URLField(blank=True, default='https://www.buddy4study.com/')
    is_external = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-application_deadline']

    def __str__(self):
        return self.name
