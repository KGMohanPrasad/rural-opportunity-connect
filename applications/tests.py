from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserProfile
from opportunities.models import Job, SavedOpportunity
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from applications.models import Application
from applications.context_processors import user_opportunity_status

class QuickApplyAndContextProcessorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='applicant1',
            email='applicant@example.com',
            password='password123',
            first_name='Anitha'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            location='Madurai',
            education='bachelor'
        )
        # Internal Job
        self.internal_job = Job.objects.create(
            title='Agricultural Field Officer',
            organization='Krishi Vikas Ltd',
            location='Madurai',
            salary_min=18000,
            salary_max=24000,
            job_type='full_time',
            deadline=timezone.now().date() + timedelta(days=30),
            is_external=False
        )
        # External Job
        self.external_job = Job.objects.create(
            title='Rural Logistics & Delivery Executive',
            organization='India Post Payments',
            location='Local Beats',
            salary_min=14000,
            salary_max=22000,
            job_type='full_time',
            deadline=timezone.now().date() + timedelta(days=30),
            is_external=True,
            source_portal='National Career Service',
            source_url='https://www.ncs.gov.in/'
        )
        # Scholarship
        self.scholarship = Scholarship.objects.create(
            name='Post-Matric Scholarship Scheme',
            provider='Ministry of Social Justice',
            amount='Rs 13,500/year',
            education_level='bachelor',
            eligibility='SC/ST Students',
            income_limit='2.5 Lakhs',
            category='Welfare',
            required_documents='Aadhaar, Marksheet',
            application_deadline=timezone.now().date() + timedelta(days=60),
            is_external=False
        )
        # Scheme
        self.scheme = GovernmentScheme.objects.create(
            name='Kisan Credit Card Scheme',
            department='Ministry of Agriculture',
            category='financial',
            description='Credit support',
            target_beneficiaries='Farmers',
            benefits='4% interest loan',
            eligibility='All farmers',
            required_documents='Land docs',
            application_process='Apply at branch',
            is_external=False
        )

    def test_get_opportunity_details_internal_job(self):
        """Test details endpoint for internal opportunity"""
        response = self.client.get(reverse('opportunity_details') + f"?type=job&id={self.internal_job.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['title'], self.internal_job.title)
        self.assertFalse(data['is_external'])
        self.assertFalse(data['already_applied'])
        self.assertIn('Location', data['highlights'])

    def test_get_opportunity_details_external_job(self):
        """Test details endpoint for external opportunity"""
        response = self.client.get(reverse('opportunity_details') + f"?type=job&id={self.external_job.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['title'], self.external_job.title)
        self.assertTrue(data['is_external'])
        self.assertEqual(data['source_portal'], 'National Career Service')
        self.assertEqual(data['source_url'], 'https://www.ncs.gov.in/')

    def test_apply_internal_opportunity(self):
        """Test applying for internal opportunity saves application to DB"""
        self.client.login(username='applicant1', password='password123')
        response = self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.internal_job.id,
                'opportunity_name': self.internal_job.title,
                'organization': self.internal_job.organization,
                'applicant_phone': '9876543210',
                'applicant_location': 'Madurai',
                'cover_note': 'Ready to start immediately',
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertFalse(data['already_applied'])
        self.assertEqual(data['active_applications_count'], 1)

        # Verify DB record
        app = Application.objects.filter(user=self.profile, opportunity_id=self.internal_job.id).first()
        self.assertIsNotNone(app)
        self.assertEqual(app.applicant_phone, '9876543210')
        self.assertEqual(app.cover_note, 'Ready to start immediately')

    def test_apply_external_opportunity_enforces_portal(self):
        """Test that external opportunity returns external_portal and does not save fake internal DB record"""
        self.client.login(username='applicant1', password='password123')
        response = self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.external_job.id,
                'opportunity_name': self.external_job.title,
                'organization': self.external_job.organization,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'external_portal')
        self.assertTrue(data['is_external'])
        self.assertEqual(data['source_url'], 'https://www.ncs.gov.in/')
        self.assertFalse(Application.objects.filter(user=self.profile, opportunity_id=self.external_job.id).exists())

    def test_duplicate_quick_apply_prevention(self):
        """Test duplicate submission returns already_applied status and does not create 2nd record"""
        self.client.login(username='applicant1', password='password123')

        # First Apply
        self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.internal_job.id,
                'opportunity_name': self.internal_job.title,
                'organization': self.internal_job.organization,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Second Apply (Duplicate)
        response2 = self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.internal_job.id,
                'opportunity_name': self.internal_job.title,
                'organization': self.internal_job.organization,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        self.assertEqual(data2['status'], 'already_applied')
        self.assertTrue(data2['already_applied'])
        self.assertEqual(data2['active_applications_count'], 1)
        self.assertEqual(Application.objects.filter(user=self.profile, opportunity_id=self.internal_job.id).count(), 1)

    def test_context_processor_opportunity_status(self):
        """Test that user_opportunity_status context processor outputs correct keys"""
        Application.objects.create(
            user=self.profile,
            opportunity_type='job',
            opportunity_id=self.internal_job.id,
            opportunity_name=self.internal_job.title,
            organization=self.internal_job.organization
        )
        SavedOpportunity.objects.create(
            user=self.profile,
            opportunity_type='job',
            opportunity_id=self.internal_job.id
        )

        class MockRequest:
            user = self.user

        context = user_opportunity_status(MockRequest())
        self.assertIn(f"job_{self.internal_job.id}", context['user_applied_keys'])
        self.assertIn(f"job_{self.internal_job.id}", context['user_saved_keys'])

