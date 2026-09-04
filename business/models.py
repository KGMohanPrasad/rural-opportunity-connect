from django.db import models

class BusinessOpportunity(models.Model):
    INVESTMENT_CHOICES = [
        ('low', 'Low (< ₹1,00,000)'),
        ('medium', 'Medium (₹1,00,000 - ₹5,00,000)'),
        ('high', 'High (> ₹5,00,000)'),
    ]

    OPPORTUNITY_LEVEL = [
        ('easy', 'Easy to Start'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    investment_level = models.CharField(max_length=20, choices=INVESTMENT_CHOICES)
    opportunity_level = models.CharField(max_length=20, choices=OPPORTUNITY_LEVEL)
    required_skills = models.TextField()
    expected_income = models.CharField(max_length=200)
    market_demand = models.CharField(max_length=100)
    resources = models.TextField()
    source_portal = models.CharField(max_length=100, default='PMEGP / Startup India', blank=True)
    source_url = models.URLField(blank=True, default='https://www.startupindia.gov.in/')
    is_external = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
