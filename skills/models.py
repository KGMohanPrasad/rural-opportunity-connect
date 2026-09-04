from django.db import models

class SkillProgram(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    PRICE_TYPE = [
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE)
    price = models.CharField(max_length=100, blank=True)
    prerequisites = models.TextField(blank=True)
    certificate = models.BooleanField(default=True)
    source_portal = models.CharField(max_length=100, default='Skill India Digital', blank=True)
    source_url = models.URLField(blank=True, default='https://www.skillindiadigital.gov.in/')
    is_external = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
