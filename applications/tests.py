from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserProfile
from opportunities.models import Job, SavedOpportunity
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
        self.job = Job.objects.create(
            title='Agricultural Field Officer',
            organization='Krishi Vikas Ltd',
            location='Madurai',
            salary_min=18000,
            salary_max=24000,
            job_type='full_time',
            deadline=timezone.now().date() + timedelta(days=30)
        )

    def test_direct_quick_apply_ajax(self):
        """Test 1-click Quick Apply submission via AJAX without personal info forms"""
        self.client.login(username='applicant1', password='password123')

        response = self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.job.id,
                'opportunity_name': self.job.title,
                'organization': self.job.organization,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertFalse(data['already_applied'])
        self.assertTrue(Application.objects.filter(user=self.profile, opportunity_id=self.job.id).exists())

    def test_duplicate_quick_apply_prevention(self):
        """Test duplicate submission returns already_applied status"""
        self.client.login(username='applicant1', password='password123')

        # First Apply
        self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.job.id,
                'opportunity_name': self.job.title,
                'organization': self.job.organization,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Second Apply (Duplicate)
        response2 = self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'job',
                'opportunity_id': self.job.id,
                'opportunity_name': self.job.title,
                'organization': self.job.organization,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        self.assertEqual(data2['status'], 'already_applied')
        self.assertTrue(data2['already_applied'])
        # Only 1 application record should exist
        self.assertEqual(Application.objects.filter(user=self.profile, opportunity_id=self.job.id).count(), 1)

    def test_context_processor_opportunity_status(self):
        """Test that user_opportunity_status context processor outputs correct keys"""
        Application.objects.create(
            user=self.profile,
            opportunity_type='job',
            opportunity_id=self.job.id,
            opportunity_name=self.job.title,
            organization=self.job.organization
        )
        SavedOpportunity.objects.create(
            user=self.profile,
            opportunity_type='job',
            opportunity_id=self.job.id
        )

        class MockRequest:
            user = self.user

        context = user_opportunity_status(MockRequest())
        self.assertIn(f"job_{self.job.id}", context['user_applied_keys'])
        self.assertIn(f"job_{self.job.id}", context['user_saved_keys'])
