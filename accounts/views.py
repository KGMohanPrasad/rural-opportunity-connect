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

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

@ensure_csrf_cookie
def landing_page(request):
    """Landing page with dynamic counts of all opportunity sectors"""
    jobs_count = Job.objects.count()
    scholarships_count = Scholarship.objects.count()
    schemes_count = GovernmentScheme.objects.count()
    skills_count = SkillProgram.objects.count()
    business_count = BusinessOpportunity.objects.count()
    total_opportunities = jobs_count + scholarships_count + schemes_count + skills_count + business_count

    context = {
        'total_opportunities': total_opportunities,
        'jobs_count': jobs_count,
        'scholarships_count': scholarships_count,
        'schemes_count': schemes_count,
        'skills_count': skills_count,
        'business_count': business_count,
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
        UserProfile.objects.create(user=user)
        DocumentChecklist.objects.create(user=UserProfile.objects.get(user=user))
        
        login(request, user)
        return redirect('profile_setup')
    
    return render(request, 'register.html')

@ensure_csrf_cookie
@csrf_protect
def login_view(request):
    """User login view with preserved next redirect"""
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url and next_url.startswith('/') and not next_url.startswith('/login') and not next_url.startswith('/logout'):
                return redirect(next_url)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password. Please try again.',
                'next_url': next_url
            })
    
    return render(request, 'login.html', {'next_url': next_url})

def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('landing_page')

@login_required(login_url='login')
def profile_setup(request):
    """Profile setup wizard"""
    profile = UserProfile.objects.get(user=request.user)
    
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
    profile = UserProfile.objects.get(user=request.user)
    
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
    profile = UserProfile.objects.get(user=request.user)
    
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

@login_required(login_url='login')
def saved_opportunities(request):
    """View saved wishlist opportunities with sector filtering"""
    profile = UserProfile.objects.get(user=request.user)
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
    }
    return render(request, 'saved_opportunities.html', context)

@login_required(login_url='login')
def application_tracker(request):
    """Track user application pipeline with stage-wise metric counters"""
    profile = UserProfile.objects.get(user=request.user)
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
    }
    return render(request, 'application_tracker.html', context)

@login_required(login_url='login')
def document_checklist(request):
    """Digital document readiness checklist with verification score"""
    profile = UserProfile.objects.get(user=request.user)
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
    }
    return render(request, 'document_checklist.html', context)

@login_required(login_url='login')
@require_http_methods(['POST'])
def save_opportunity(request):
    """Save/unsave an opportunity bookmark"""
    profile = UserProfile.objects.get(user=request.user)
    opp_type = request.POST.get('type')
    opp_id = request.POST.get('id')
    
    try:
        saved = SavedOpportunity.objects.get(
            user=profile,
            opportunity_type=opp_type,
            opportunity_id=opp_id
        )
        saved.delete()
        return JsonResponse({'status': 'removed'})
    except SavedOpportunity.DoesNotExist:
        SavedOpportunity.objects.create(
            user=profile,
            opportunity_type=opp_type,
            opportunity_id=opp_id
        )
        return JsonResponse({'status': 'saved'})

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

