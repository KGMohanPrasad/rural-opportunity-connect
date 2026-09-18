from django.db import models
from accounts.models import UserProfile

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    OPPORTUNITY_TYPE = [
        ('job', 'Job'),
        ('scholarship', 'Scholarship'),
        ('scheme', 'Government Scheme'),
        ('skill', 'Skill Program'),
        ('business', 'Business Opportunity'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE)
    opportunity_id = models.IntegerField()
    opportunity_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applicant_phone = models.CharField(max_length=25, blank=True, default='')
    applicant_location = models.CharField(max_length=100, blank=True, default='')
    cover_note = models.TextField(blank=True, default='')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.user.user.username} - {self.opportunity_name}"


class DocumentChecklist(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='document_checklist')
    aadhaar = models.BooleanField(default=False)
    marksheet = models.BooleanField(default=False)
    income_certificate = models.BooleanField(default=False)
    community_certificate = models.BooleanField(default=False)
    bank_details = models.BooleanField(default=False)
    residence_certificate = models.BooleanField(default=False)
    passport = models.BooleanField(default=False)
    pan_card = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Documents for {self.user.user.username}"

    def documents_ready_count(self):
        fields = [
            self.aadhaar, self.marksheet, self.income_certificate,
            self.community_certificate, self.bank_details, self.residence_certificate,
            self.passport, self.pan_card
        ]
        return sum(1 for field in fields if field)
