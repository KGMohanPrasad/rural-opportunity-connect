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
    source_portal = models.CharField(max_length=120, blank=True, default='')
    source_url = models.URLField(max_length=500, blank=True, default='')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.user.user.username} - {self.opportunity_name}"

    def get_opportunity(self):
        try:
            if self.opportunity_type == 'job':
                from opportunities.models import Job
                return Job.objects.filter(id=self.opportunity_id).first()
            elif self.opportunity_type == 'scholarship':
                from scholarships.models import Scholarship
                return Scholarship.objects.filter(id=self.opportunity_id).first()
            elif self.opportunity_type == 'scheme':
                from government_schemes.models import GovernmentScheme
                return GovernmentScheme.objects.filter(id=self.opportunity_id).first()
            elif self.opportunity_type == 'skill':
                from skills.models import SkillProgram
                return SkillProgram.objects.filter(id=self.opportunity_id).first()
            elif self.opportunity_type == 'business':
                from business.models import BusinessOpportunity
                return BusinessOpportunity.objects.filter(id=self.opportunity_id).first()
        except Exception:
            return None
        return None

    def get_partner_url(self):
        if self.source_url:
            return self.source_url
        opp = self.get_opportunity()
        if opp:
            return getattr(opp, 'source_url', '') or getattr(opp, 'official_url', '') or getattr(opp, 'apply_url', '')
        return ''

    def get_partner_name(self):
        if self.source_portal:
            return self.source_portal
        opp = self.get_opportunity()
        if opp:
            return getattr(opp, 'source_portal', '') or getattr(opp, 'department', '') or getattr(opp, 'provider', '') or self.organization
        return self.organization or 'Official Partner'


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
