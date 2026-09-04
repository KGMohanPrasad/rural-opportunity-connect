from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserProfile
from applications.models import DocumentChecklist, Application
from opportunities.models import Job, SavedOpportunity
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from skills.models import SkillProgram
from business.models import BusinessOpportunity

class RuralOpportunityConnectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='Ramesh',
            last_name='Kumar'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            age=22,
            location='Tamil Nadu',
            education='bachelor',
            course='B.Sc Agriculture',
            skills='Agriculture, Python, Typing',
            experience='1 year farm work',
            annual_income='< 1.5 Lakhs',
            interests='Farming, Technology',
            preferred_opportunity='jobs'
        )
        self.checklist = DocumentChecklist.objects.create(
            user=self.profile,
            aadhaar=True,
            marksheet=True
        )

        # Create sample data
        self.job = Job.objects.create(
            title='Junior Farm Assistant',
            organization='Green Agro Ltd',
            description='Field management role.',
            location='Tamil Nadu',
            salary_min=15000,
            salary_max=20000,
            job_type='full_time',
            required_skills='Agriculture, Physical Fitness',
            experience_required='Fresher',
            deadline=timezone.now().date() + timedelta(days=30)
        )

        self.scholarship = Scholarship.objects.create(
            name='Rural Higher Education Grant',
            provider='State Education Board',
            description='Scholarship for degree students.',
            amount='₹25,000 / year',
            education_level='bachelor',
            eligibility='Annual family income under 2 Lakhs',
            income_limit='< 2 Lakhs',
            category='Merit-cum-Means',
            required_documents='Aadhaar, Marksheet',
            application_deadline=timezone.now().date() + timedelta(days=40)
        )

        self.scheme = GovernmentScheme.objects.create(
            name='Kisan Credit & Subsidy Scheme',
            department='Ministry of Agriculture',
            category='agriculture',
            description='Financial assistance for farmers.',
            target_beneficiaries='Small and marginal farmers',
            benefits='Subsidized seeds and credit up to ₹1,00,000',
            eligibility='Rural landholder or tenant farmer',
            required_documents='Aadhaar, Land records',
            application_process='Apply at nearest Gram Panchayat or online',
            official_website='https://example.gov.in'
        )

        self.skill = SkillProgram.objects.create(
            name='Digital Agriculture & Soil Testing',
            category='agricultural',
            provider='Krishi Vigyan Kendra',
            description='Hands-on training in modern soil health testing.',
            duration='4 Weeks',
            level='beginner',
            price_type='free',
            certificate=True
        )

        self.business = BusinessOpportunity.objects.create(
            name='Organic Vermicompost Production',
            category='agriculture',
            description='Low-cost organic fertilizer manufacturing unit.',
            investment_level='low',
            opportunity_level='easy',
            required_skills='Basic composting knowledge',
            expected_income='₹20,000 - ₹40,000 / month',
            market_demand='High in rural districts',
            resources='Raw biomass, earthworms, shed'
        )

    def test_public_pages_render(self):
        """Test public catalog and landing pages render with 200 OK"""
        routes = [
            'landing_page',
            'about',
            'partners',
            'jobs_list',
            'scholarships_list',
            'schemes_list',
            'skills_list',
            'business_list',
            'login',
            'register',
        ]
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200, f"Route '{route}' failed with status {response.status_code}")

    def test_external_sync_service(self):
        """Test ExternalIntegrationsService synchronizes opportunities from Buddy4Study, myScheme, NSP, NCS"""
        from services.external_integrations import ExternalIntegrationsService
        results = ExternalIntegrationsService.sync_all()
        self.assertGreater(results['buddy4study'], 0)
        self.assertGreater(results['myscheme'], 0)
        self.assertGreater(results['total_synced'], 0)
        self.assertTrue(Scholarship.objects.filter(source_portal__icontains='Buddy4Study').exists())

    def test_sync_partners_api(self):
        """Test /api/sync-partners/ endpoint"""
        res = self.client.post(reverse('sync_partners_api'), {'source': 'buddy4study'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')

    def test_detail_pages_render(self):
        """Test detail views for all 5 sectors"""
        job_res = self.client.get(reverse('job_detail', args=[self.job.id]))
        self.assertEqual(job_res.status_code, 200)

        sch_res = self.client.get(reverse('scholarship_detail', args=[self.scholarship.id]))
        self.assertEqual(sch_res.status_code, 200)

        scheme_res = self.client.get(reverse('scheme_detail', args=[self.scheme.id]))
        self.assertEqual(scheme_res.status_code, 200)

        skill_res = self.client.get(reverse('skill_detail', args=[self.skill.id]))
        self.assertEqual(skill_res.status_code, 200)

        biz_res = self.client.get(reverse('business_detail', args=[self.business.id]))
        self.assertEqual(biz_res.status_code, 200)

    def test_landing_page_dynamic_stats(self):
        """Test that landing page context contains dynamic opportunity counts"""
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_opportunities', response.context)
        self.assertGreaterEqual(response.context['total_opportunities'], 5)

    def test_authenticated_user_pages(self):
        """Test user dashboard, profile, checklist, and tracker when logged in"""
        self.client.login(username='testuser', password='password123')

        routes = [
            'dashboard',
            'profile',
            'profile_setup',
            'saved_opportunities',
            'applications',
            'document_checklist',
        ]
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200, f"Authenticated route '{route}' failed with {response.status_code}")

    def test_save_opportunity_toggle(self):
        """Test saving and removing an opportunity"""
        self.client.login(username='testuser', password='password123')
        
        # Save
        res = self.client.post(reverse('save_opportunity'), {'type': 'job', 'id': self.job.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'saved')
        self.assertTrue(SavedOpportunity.objects.filter(user=self.profile, opportunity_type='job', opportunity_id=self.job.id).exists())

        # Unsave
        res2 = self.client.post(reverse('save_opportunity'), {'type': 'job', 'id': self.job.id})
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.json()['status'], 'removed')
        self.assertFalse(SavedOpportunity.objects.filter(user=self.profile, opportunity_type='job', opportunity_id=self.job.id).exists())

    def test_apply_opportunity(self):
        """Test application submission creates Application record"""
        self.client.login(username='testuser', password='password123')
        
        res = self.client.post(reverse('apply_opportunity'), {
            'opportunity_type': 'job',
            'opportunity_id': self.job.id,
            'opportunity_name': self.job.title,
            'organization': self.job.organization
        }, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Application.objects.filter(user=self.profile, opportunity_id=self.job.id).exists())

    def test_apply_opportunity_ajax(self):
        """Test application submission via AJAX modal returns JSON success"""
        self.client.login(username='testuser', password='password123')

        res = self.client.post(
            reverse('apply_opportunity'),
            {
                'opportunity_type': 'scholarship',
                'opportunity_id': self.scholarship.id,
                'opportunity_name': self.scholarship.name,
                'organization': self.scholarship.provider,
                'is_ajax': '1'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertTrue(Application.objects.filter(user=self.profile, opportunity_id=self.scholarship.id).exists())

    def test_document_checklist_update(self):
        """Test document readiness update"""
        self.client.login(username='testuser', password='password123')
        
        res = self.client.post(reverse('document_checklist'), {
            'aadhaar': 'on',
            'marksheet': 'on',
            'income_certificate': 'on',
            'pan_card': 'on'
        }, follow=True)

        self.assertEqual(res.status_code, 200)
        self.checklist.refresh_from_db()
        self.assertTrue(self.checklist.income_certificate)
        self.assertTrue(self.checklist.pan_card)
        self.assertEqual(self.checklist.documents_ready_count(), 4)

    def test_login_with_next_redirect(self):
        """Test that logging in with next parameter redirects back to target opportunity page"""
        login_page = self.client.get(reverse('login') + '?next=/jobs/')
        self.assertEqual(login_page.status_code, 200)
        self.assertIn('csrftoken', login_page.cookies)

        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'password123',
                'next': '/jobs/'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/jobs/')

    def test_saved_opportunities_filtering(self):
        """Test filtering saved items by category"""
        self.client.login(username='testuser', password='password123')
        # Save a job and a scholarship
        SavedOpportunity.objects.create(user=self.profile, opportunity_type='job', opportunity_id=self.job.id)
        SavedOpportunity.objects.create(user=self.profile, opportunity_type='scholarship', opportunity_id=self.scholarship.id)

        # Filter by job
        res_job = self.client.get(reverse('saved_opportunities') + '?type=job')
        self.assertEqual(res_job.status_code, 200)
        self.assertEqual(len(res_job.context['saved_items']), 1)
        self.assertEqual(res_job.context['saved_items'][0]['type'], 'job')

        # Filter by all
        res_all = self.client.get(reverse('saved_opportunities') + '?type=all')
        self.assertEqual(res_all.status_code, 200)
        self.assertEqual(len(res_all.context['saved_items']), 2)

    def test_application_tracker_counters(self):
        """Test pipeline metric counters in application tracker"""
        self.client.login(username='testuser', password='password123')
        Application.objects.create(
            user=self.profile, opportunity_type='job', opportunity_id=self.job.id,
            opportunity_name=self.job.title, organization=self.job.organization, status='under_review'
        )
        Application.objects.create(
            user=self.profile, opportunity_type='scholarship', opportunity_id=self.scholarship.id,
            opportunity_name=self.scholarship.name, organization=self.scholarship.provider, status='shortlisted'
        )

        res = self.client.get(reverse('applications'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['total_applications'], 2)
        self.assertEqual(res.context['under_review_count'], 1)
        self.assertEqual(res.context['shortlisted_count'], 1)
        self.assertEqual(res.context['selected_count'], 0)

    def test_recommendation_service_scores(self):
        """Test intelligent recommendation service outputs match scores and reasons"""
        from services.recommendation_service import RecommendationService
        recs = RecommendationService.get_recommendations(self.profile)
        self.assertIn('jobs', recs)
        self.assertIn('scholarships', recs)
        self.assertIn('schemes', recs)
        self.assertIn('skills', recs)
        self.assertIn('business', recs)
        if recs['jobs']:
            self.assertIn('match_score', recs['jobs'][0])
            self.assertGreaterEqual(recs['jobs'][0]['match_score'], 50)
            self.assertIn('match_reasons', recs['jobs'][0])
