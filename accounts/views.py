from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from accounts.models import UserProfile
from applications.models import DocumentChecklist, Application
from opportunities.models import SavedOpportunity, Job
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from skills.models import SkillProgram
from business.models import BusinessOpportunity
import requests

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.db.models import Q

@ensure_csrf_cookie
def landing_page(request):
    """Landing page with dynamic counts of all opportunity sectors"""
    jobs_count = Job.objects.count()
    scholarships_count = Scholarship.objects.count()
    schemes_count = GovernmentScheme.objects.count()
    skills_count = SkillProgram.objects.count()
    business_count = BusinessOpportunity.objects.count()
    total_opportunities = jobs_count + scholarships_count + schemes_count + skills_count + business_count

    featured_job = Job.objects.order_by('id').first()
    featured_scholarship = Scholarship.objects.order_by('id').first()
    featured_scheme = GovernmentScheme.objects.order_by('id').first()

    context = {
        'total_opportunities': total_opportunities,
        'jobs_count': jobs_count,
        'scholarships_count': scholarships_count,
        'schemes_count': schemes_count,
        'skills_count': skills_count,
        'business_count': business_count,
        'featured_job': featured_job,
        'featured_scholarship': featured_scholarship,
        'featured_scheme': featured_scheme,
    }
    return render(request, 'landing.html', context)

@ensure_csrf_cookie
@csrf_protect
def register(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        user_profile = UserProfile.objects.create(user=user)
        DocumentChecklist.objects.create(user=user_profile)
        
        # Migrate any guest applications or wishlist items to this newly registered user
        try:
            guest_user = User.objects.filter(username='guest_candidate').first()
            if guest_user and guest_user.id != user.id:
                guest_profile = UserProfile.objects.filter(user=guest_user).first()
                if guest_profile:
                    for guest_app in Application.objects.filter(user=guest_profile):
                        if not Application.objects.filter(user=user_profile, opportunity_type=guest_app.opportunity_type, opportunity_id=guest_app.opportunity_id).exists():
                            guest_app.user = user_profile
                            guest_app.save()
                    for guest_saved in SavedOpportunity.objects.filter(user=guest_profile):
                        if not SavedOpportunity.objects.filter(user=user_profile, opportunity_type=guest_saved.opportunity_type, opportunity_id=guest_saved.opportunity_id).exists():
                            guest_saved.user = user_profile
                            guest_saved.save()
        except Exception:
            pass

        login(request, user)
        return redirect('profile_setup')
    
    return render(request, 'register.html')

@ensure_csrf_cookie
@csrf_protect
def login_view(request):
    """User login view with username or email authentication and guest migration"""
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        login_input = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # 1. Try direct username auth
        user = authenticate(request, username=login_input, password=password)
        
        # 2. If not found, check if login_input is an email
        if user is None:
            user_by_email = User.objects.filter(email__iexact=login_input).first()
            if user_by_email:
                user = authenticate(request, username=user_by_email.username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Migrate any guest applications or wishlist items to this user's profile
            try:
                guest_user = User.objects.filter(username='guest_candidate').first()
                if guest_user and guest_user.id != user.id:
                    guest_profile = UserProfile.objects.filter(user=guest_user).first()
                    user_profile, _ = UserProfile.objects.get_or_create(user=user)
                    if guest_profile:
                        # Migrate guest applications
                        for guest_app in Application.objects.filter(user=guest_profile):
                            if not Application.objects.filter(user=user_profile, opportunity_type=guest_app.opportunity_type, opportunity_id=guest_app.opportunity_id).exists():
                                guest_app.user = user_profile
                                guest_app.save()
                        # Migrate guest wishlist items
                        for guest_saved in SavedOpportunity.objects.filter(user=guest_profile):
                            if not SavedOpportunity.objects.filter(user=user_profile, opportunity_type=guest_saved.opportunity_type, opportunity_id=guest_saved.opportunity_id).exists():
                                guest_saved.user = user_profile
                                guest_saved.save()
            except Exception:
                pass

            if next_url and next_url.startswith('/') and not next_url.startswith('/login') and not next_url.startswith('/logout'):
                return redirect(next_url)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password. Please try again.',
                'next_url': next_url,
                'entered_username': login_input
            })
    
    return render(request, 'login.html', {'next_url': next_url})

def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('landing_page')

@login_required(login_url='login')
def profile_setup(request):
    """Profile setup wizard"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.age = request.POST.get('age')
        profile.location = request.POST.get('location')
        profile.education = request.POST.get('education')
        profile.course = request.POST.get('course')
        profile.skills = request.POST.get('skills')
        profile.experience = request.POST.get('experience')
        profile.annual_income = request.POST.get('annual_income')
        profile.interests = request.POST.get('interests')
        profile.preferred_opportunity = request.POST.get('preferred_opportunity')
        profile.save()
        
        return redirect('dashboard')
    
    context = {
        'profile': profile,
        'education_choices': UserProfile.EDUCATION_CHOICES,
        'opportunity_choices': UserProfile.INTEREST_CHOICES,
    }
    return render(request, 'profile_setup.html', context)

from services.recommendation_service import RecommendationService

@login_required(login_url='login')
def dashboard(request):
    """User dashboard with personalized recommendations and progress metrics"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    # Get intelligent recommendations from microservice or local service
    recommendations = RecommendationService.get_recommendations(profile)
    
    saved_count = SavedOpportunity.objects.filter(user=profile).count()
    applications_count = Application.objects.filter(user=profile).count()
    completion_pct = profile.profile_completion_percentage()
    
    context = {
        'profile': profile,
        'recommendations': recommendations,
        'saved_count': saved_count,
        'applications_count': applications_count,
        'completion_percentage': completion_pct,
        'profile_percentage': completion_pct,
    }
    
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profile_view(request):
    """View and edit user profile with live profile strength score"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.age = request.POST.get('age') or None
        profile.location = request.POST.get('location', '').strip()
        profile.education = request.POST.get('education', '').strip()
        profile.course = request.POST.get('course', '').strip()
        profile.skills = request.POST.get('skills', '').strip()
        profile.experience = request.POST.get('experience', '').strip()
        profile.annual_income = request.POST.get('annual_income', '').strip()
        profile.interests = request.POST.get('interests', '').strip()
        profile.preferred_opportunity = request.POST.get('preferred_opportunity', '').strip()
        profile.save()
        
        return redirect('profile')
    
    completion_pct = profile.profile_completion_percentage()
    context = {
        'profile': profile,
        'education_choices': UserProfile.EDUCATION_CHOICES,
        'opportunity_choices': UserProfile.INTEREST_CHOICES,
        'completion_percentage': completion_pct,
        'profile_percentage': completion_pct,
    }
    return render(request, 'profile.html', context)

def get_active_profile(request):
    """Helper to get UserProfile for authenticated user or guest candidate session"""
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return profile, False
    guest_user, _ = User.objects.get_or_create(
        username='guest_candidate',
        defaults={
            'first_name': 'Guest',
            'last_name': 'Candidate',
            'email': 'guest@ruralopportunity.org'
        }
    )
    profile, _ = UserProfile.objects.get_or_create(user=guest_user)
    return profile, True

def saved_opportunities(request):
    """View saved wishlist opportunities with sector filtering for users and guests"""
    profile, is_guest = get_active_profile(request)
    active_type = request.GET.get('type', 'all').strip().lower()
    
    all_saved = SavedOpportunity.objects.filter(user=profile).order_by('-saved_at')
    total_count = all_saved.count()

    if active_type and active_type != 'all':
        saved_opps = all_saved.filter(opportunity_type=active_type)
    else:
        saved_opps = all_saved
    
    # Fetch details for saved opportunities
    opportunities = []
    for saved in saved_opps:
        obj = get_opportunity_object(saved.opportunity_type, saved.opportunity_id)
        if obj:
            title = getattr(obj, 'title', None) or getattr(obj, 'name', 'Opportunity')
            org = getattr(obj, 'organization', None) or getattr(obj, 'provider', None) or getattr(obj, 'department', '')
            detail_url = ''
            if saved.opportunity_type == 'job':
                detail_url = f'/jobs/{obj.id}/'
            elif saved.opportunity_type == 'scholarship':
                detail_url = f'/scholarships/{obj.id}/'
            elif saved.opportunity_type == 'scheme':
                detail_url = f'/schemes/{obj.id}/'
            elif saved.opportunity_type == 'skill':
                detail_url = f'/skills/{obj.id}/'
            elif saved.opportunity_type == 'business':
                detail_url = f'/business/{obj.id}/'

            opportunities.append({
                'id': obj.id,
                'saved_id': saved.id,
                'type': saved.opportunity_type,
                'type_display': saved.get_opportunity_type_display(),
                'title': title,
                'organization': org,
                'description': getattr(obj, 'description', ''),
                'saved_at': saved.saved_at,
                'detail_url': detail_url,
                'obj': obj
            })
    
    context = {
        'saved_items': opportunities,
        'opportunities': opportunities,
        'total_count': total_count,
        'active_type': active_type,
        'is_guest': is_guest,
    }
    return render(request, 'saved_opportunities.html', context)

def application_tracker(request):
    """Track user and guest application pipeline with stage-wise metric counters"""
    profile, is_guest = get_active_profile(request)
    applications = Application.objects.filter(user=profile).order_by('-applied_date')
    
    total_applications = applications.count()
    under_review_count = applications.filter(status='under_review').count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    selected_count = applications.filter(status__in=['selected', 'interview']).count()
    rejected_count = applications.filter(status='rejected').count()
    
    context = {
        'applications': applications,
        'total_applications': total_applications,
        'under_review_count': under_review_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'is_guest': is_guest,
    }
    return render(request, 'application_tracker.html', context)

def document_checklist(request):
    """Digital document readiness checklist with verification score for users and guests"""
    profile, is_guest = get_active_profile(request)
    checklist, _ = DocumentChecklist.objects.get_or_create(user=profile)
    
    if request.method == 'POST':
        checklist.aadhaar = request.POST.get('aadhaar') == 'on'
        checklist.marksheet = request.POST.get('marksheet') == 'on'
        checklist.income_certificate = request.POST.get('income_certificate') == 'on'
        checklist.community_certificate = (request.POST.get('community_certificate') == 'on' or request.POST.get('caste_certificate') == 'on')
        checklist.bank_details = request.POST.get('bank_details') == 'on'
        checklist.residence_certificate = request.POST.get('residence_certificate') == 'on'
        checklist.passport = request.POST.get('passport') == 'on'
        checklist.pan_card = request.POST.get('pan_card') == 'on'
        checklist.save()
        
        return redirect('document_checklist')
    
    ready_count = checklist.documents_ready_count()
    percentage = int((ready_count / 8) * 100)
    
    context = {
        'checklist': checklist,
        'ready_count': ready_count,
        'documents_ready': ready_count,
        'total_documents': 8,
        'percentage': percentage,
        'is_guest': is_guest,
    }
    return render(request, 'document_checklist.html', context)

@csrf_exempt
@require_http_methods(['POST'])
def save_opportunity(request):
    """Save/unsave an opportunity bookmark for authenticated or guest users"""
    profile, is_guest = get_active_profile(request)
    opp_type = request.POST.get('type')
    opp_id = request.POST.get('id')
    
    try:
        saved = SavedOpportunity.objects.get(
            user=profile,
            opportunity_type=opp_type,
            opportunity_id=opp_id
        )
        saved.delete()
        return JsonResponse({'status': 'removed', 'is_saved': False})
    except SavedOpportunity.DoesNotExist:
        SavedOpportunity.objects.create(
            user=profile,
            opportunity_type=opp_type,
            opportunity_id=opp_id
        )
        return JsonResponse({'status': 'saved', 'is_saved': True})

def get_recommendations(profile):
    """Get personalized recommendations from RecommendationService"""
    return RecommendationService.get_recommendations(profile)

def get_opportunity_object(opp_type, opp_id):
    """Get actual model object of an opportunity by type"""
    try:
        if opp_type == 'job':
            return Job.objects.get(id=opp_id)
        elif opp_type == 'scholarship':
            return Scholarship.objects.get(id=opp_id)
        elif opp_type == 'scheme':
            return GovernmentScheme.objects.get(id=opp_id)
        elif opp_type == 'skill':
            return SkillProgram.objects.get(id=opp_id)
        elif opp_type == 'business':
            return BusinessOpportunity.objects.get(id=opp_id)
    except Exception:
        return None

def about_page(request):
    """About page with Design Thinking and SDG info"""
    return render(request, 'about.html')

def partners_view(request):
    """Connected Apps & Opportunity Portals Directory (Buddy4Study, myScheme, NSP, Skill India, etc.)"""
    from services.external_integrations import ExternalIntegrationsService
    portals = ExternalIntegrationsService.get_connected_portals()
    
    total_external_count = (
        Scholarship.objects.filter(is_external=True).count() +
        GovernmentScheme.objects.filter(is_external=True).count() +
        Job.objects.filter(is_external=True).count() +
        SkillProgram.objects.filter(is_external=True).count() +
        BusinessOpportunity.objects.filter(is_external=True).count()
    )

    context = {
        'portals': portals,
        'total_external_count': total_external_count,
        'buddy4study_scholarships': Scholarship.objects.filter(source_portal__icontains='Buddy4Study')[:4],
        'myscheme_schemes': GovernmentScheme.objects.filter(source_portal__icontains='myScheme')[:4],
        'ncs_jobs': Job.objects.filter(source_portal__icontains='National Career Service')[:4],
        'skillindia_courses': SkillProgram.objects.filter(source_portal__icontains='Skill India')[:4],
    }
    return render(request, 'partners.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sync_partners_api(request):
    """On-demand trigger to fetch/sync external opportunity feeds"""
    if request.method == 'POST':
        from services.external_integrations import ExternalIntegrationsService
        source = request.POST.get('source', 'all')
        if source == 'buddy4study':
            count = ExternalIntegrationsService.sync_buddy4study_scholarships()
            return JsonResponse({'status': 'success', 'message': f'Synchronized {count} Buddy4Study scholarships.'})
        else:
            results = ExternalIntegrationsService.sync_all()
            return JsonResponse({
                'status': 'success',
                'message': f"Synchronized {results['total_synced']} external opportunities across all networks.",
                'results': results
            })
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

def custom_404(request, exception=None):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 error page"""
    return render(request, '500.html', status=500)


def quick_search_api(request):
    """Universal Quick Search endpoint for Quick Access Hub"""
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})

    results = []

    # 1. Search Jobs
    jobs = Job.objects.filter(
        Q(title__icontains=q) | Q(organization__icontains=q) | Q(required_skills__icontains=q) | Q(location__icontains=q)
    )[:6]
    for j in jobs:
        sal = f"₹{j.salary_min:,} - ₹{j.salary_max:,}/mo" if j.salary_min and j.salary_max else "Competitive"
        results.append({
            'type': 'Job',
            'category': 'jobs',
            'applyType': 'job',
            'id': j.id,
            'title': j.title,
            'org': j.organization,
            'meta': f"{j.location} • {sal}",
            'detail_url': f"/jobs/{j.id}/",
            'badge_color': 'blue'
        })

    # 2. Search Scholarships
    scholarships = Scholarship.objects.filter(
        Q(name__icontains=q) | Q(provider__icontains=q) | Q(eligibility__icontains=q)
    )[:5]
    for sc in scholarships:
        results.append({
            'type': 'Scholarship',
            'category': 'scholarships',
            'applyType': 'scholarship',
            'id': sc.id,
            'title': sc.name,
            'org': sc.provider,
            'meta': sc.amount or "Merit Grant",
            'detail_url': f"/scholarships/{sc.id}/",
            'badge_color': 'amber'
        })

    # 3. Search Government Schemes
    schemes = GovernmentScheme.objects.filter(
        Q(name__icontains=q) | Q(department__icontains=q) | Q(description__icontains=q) | Q(benefits__icontains=q)
    )[:5]
    for s in schemes:
        benefit_preview = s.benefits[:45] + '...' if len(s.benefits) > 45 else s.benefits
        results.append({
            'type': 'Scheme',
            'category': 'schemes',
            'applyType': 'scheme',
            'id': s.id,
            'title': s.name,
            'org': s.department,
            'meta': benefit_preview or "Govt Welfare Subsidy",
            'detail_url': f"/schemes/{s.id}/",
            'badge_color': 'emerald'
        })

    # 4. Search Skills
    skills = SkillProgram.objects.filter(
        Q(name__icontains=q) | Q(provider__icontains=q) | Q(category__icontains=q)
    )[:5]
    for sk in skills:
        results.append({
            'type': 'Skill',
            'category': 'skills',
            'applyType': 'skill',
            'id': sk.id,
            'title': sk.name,
            'org': sk.provider,
            'meta': f"{sk.duration} • {sk.get_level_display() if hasattr(sk, 'get_level_display') else sk.level}",
            'detail_url': f"/skills/{sk.id}/",
            'badge_color': 'purple'
        })

    # 5. Search Business Opportunities
    businesses = BusinessOpportunity.objects.filter(
        Q(name__icontains=q) | Q(category__icontains=q) | Q(description__icontains=q)
    )[:5]
    for b in businesses:
        results.append({
            'type': 'Business',
            'category': 'business',
            'applyType': 'business',
            'id': b.id,
            'title': b.name,
            'org': b.category,
            'meta': b.expected_income or "Micro-Enterprise Plan",
            'detail_url': f"/business/{b.id}/",
            'badge_color': 'orange'
        })

    return JsonResponse({'results': results[:15]})

