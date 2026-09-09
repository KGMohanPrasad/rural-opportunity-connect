from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from accounts.models import UserProfile
from opportunities.models import Job
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from skills.models import SkillProgram
from business.models import BusinessOpportunity
from .models import Application

def get_opportunity_details(request):
    """
    Returns verified real-time metadata and current application status for any opportunity.
    Used by the unified Quick Apply modal to dynamically render Flow 1 (Internal) or Flow 2 (External).
    """
    opp_type = (request.GET.get('type') or 'job').strip().lower()
    try:
        opp_id = int(request.GET.get('id') or 0)
    except (ValueError, TypeError):
        opp_id = 0

    if opp_id <= 0:
        return JsonResponse({'status': 'error', 'message': 'Invalid opportunity ID.'}, status=400)

    obj = None
    title = ''
    organization = ''
    is_external = False
    source_portal = ''
    source_url = ''
    type_display = 'Opportunity'
    highlights = {}

    if opp_type == 'job':
        obj = Job.objects.filter(id=opp_id).first()
        if obj:
            title = obj.title
            organization = obj.organization
            is_external = bool(obj.is_external)
            source_portal = obj.source_portal or 'National Career Service'
            source_url = obj.source_url or 'https://www.ncs.gov.in/'
            type_display = 'Job Opening'
            highlights = {
                'Location': obj.location or 'Multiple Rural Centers',
                'Monthly Salary': f"₹{obj.salary_min:,} - ₹{obj.salary_max:,}" if obj.salary_min else 'Competitive Scale',
                'Job Type': obj.get_job_type_display(),
                'Experience': obj.experience_required or 'Freshers / Rural Youth Welcome',
                'Application Deadline': obj.deadline.strftime('%b %d, %Y') if obj.deadline else 'Open Until Filled'
            }
    elif opp_type == 'scholarship':
        obj = Scholarship.objects.filter(id=opp_id).first()
        if obj:
            title = obj.name
            organization = obj.provider
            is_external = bool(obj.is_external)
            source_portal = obj.source_portal or 'National Scholarship Portal'
            source_url = obj.source_url or 'https://scholarships.gov.in/'
            type_display = 'Higher Education Scholarship'
            highlights = {
                'Financial Grant': obj.amount or 'Direct Benefit Transfer (DBT)',
                'Target Education': obj.get_education_level_display(),
                'Category / Stream': obj.category or 'All Eligible Students',
                'Income Ceiling': obj.income_limit or 'Standard Norms',
                'Submission Deadline': obj.application_deadline.strftime('%b %d, %Y') if obj.application_deadline else 'Active'
            }
    elif opp_type == 'scheme':
        obj = GovernmentScheme.objects.filter(id=opp_id).first()
        if obj:
            title = obj.name
            organization = obj.department
            is_external = bool(obj.is_external)
            source_portal = obj.source_portal or 'myScheme.gov.in'
            source_url = obj.source_url or obj.official_website or 'https://www.myscheme.gov.in/'
            type_display = 'Government Welfare Scheme'
            highlights = {
                'Administering Dept': obj.department,
                'Beneficiary Coverage': (obj.target_beneficiaries[:110] + '...') if len(obj.target_beneficiaries) > 110 else obj.target_beneficiaries,
                'Category': obj.get_category_display(),
                'Scheme Benefits': (obj.benefits[:110] + '...') if len(obj.benefits) > 110 else obj.benefits,
            }
    elif opp_type == 'skill':
        obj = SkillProgram.objects.filter(id=opp_id).first()
        if obj:
            title = obj.name
            organization = obj.provider
            is_external = bool(obj.is_external)
            source_portal = obj.source_portal or 'Skill India Digital'
            source_url = obj.source_url or 'https://www.skillindiadigital.gov.in/'
            type_display = 'Skill Development Program'
            highlights = {
                'Training Provider': obj.provider,
                'Program Duration': obj.duration,
                'Proficiency Level': obj.get_level_display(),
                'Certification': 'NSDC / Government Certified' if obj.certificate else 'Course Completion',
                'Course Fee': '100% Free / Subsidized' if obj.price_type == 'free' else (obj.price or 'Affordable Fee')
            }
    elif opp_type == 'business':
        obj = BusinessOpportunity.objects.filter(id=opp_id).first()
        if obj:
            title = obj.name
            organization = 'Micro-Enterprise Track'
            is_external = bool(obj.is_external)
            source_portal = obj.source_portal or 'PMEGP / Startup India'
            source_url = obj.source_url or 'https://www.startupindia.gov.in/'
            type_display = 'Artisan & Micro-Enterprise'
            highlights = {
                'Capital Required': obj.get_investment_level_display(),
                'Expected Income': obj.expected_income,
                'Market Demand': obj.market_demand,
                'Ease of Launch': obj.get_opportunity_level_display()
            }

    if not obj:
        return JsonResponse({'status': 'error', 'message': f'Opportunity #{opp_id} not found in database.'}, status=404)

    # Check if already applied
    already_applied = False
    existing_app = None
    user_info = {
        'is_authenticated': request.user.is_authenticated,
        'full_name': '',
        'email': '',
        'phone': '',
        'location': '',
        'education': ''
    }

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_info['full_name'] = request.user.get_full_name() or request.user.username
        user_info['email'] = request.user.email
        user_info['location'] = profile.location or ''
        user_info['education'] = profile.get_education_display() if profile.education else ''
        existing_app = Application.objects.filter(user=profile, opportunity_type=opp_type, opportunity_id=opp_id).first()
        already_applied = existing_app is not None
    else:
        # Check session tracking for guest candidates
        session_applied = request.session.get('applied_keys', [])
        key = f"{opp_type}_{opp_id}"
        if key in session_applied:
            already_applied = True
            guest_user = User.objects.filter(username='guest_candidate').first()
            if guest_user:
                guest_profile = UserProfile.objects.filter(user=guest_user).first()
                if guest_profile:
                    existing_app = Application.objects.filter(user=guest_profile, opportunity_type=opp_type, opportunity_id=opp_id).first()

    return JsonResponse({
        'status': 'success',
        'id': opp_id,
        'type': opp_type,
        'type_display': type_display,
        'title': title,
        'organization': organization,
        'is_external': is_external,
        'source_portal': source_portal,
        'source_url': source_url,
        'already_applied': already_applied,
        'application_id': existing_app.id if existing_app else None,
        'applied_date': existing_app.applied_date.strftime('%B %d, %Y') if existing_app else None,
        'highlights': highlights,
        'user_info': user_info
    })


@csrf_exempt
def apply_opportunity(request):
    """
    Direct Quick Apply submission for both authenticated and guest candidates.
    Validates internal vs external opportunities, records internal applications in database,
    and reliably prevents duplicate submissions.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method. POST required.'}, status=400)

    opp_type = (request.POST.get('opportunity_type') or 'job').strip().lower()
    try:
        opp_id = int(request.POST.get('opportunity_id') or 0)
    except (ValueError, TypeError):
        opp_id = 0

    if opp_id <= 0:
        return JsonResponse({'status': 'error', 'message': 'Valid opportunity ID is required.'}, status=400)

    # Resolve target opportunity
    opp_name = (request.POST.get('opportunity_name') or '').strip()
    org = (request.POST.get('organization') or '').strip()
    is_external = False
    source_portal = ''
    source_url = ''

    if opp_type == 'job':
        job_obj = Job.objects.filter(id=opp_id).first()
        if job_obj:
            opp_name = opp_name or job_obj.title
            org = org or job_obj.organization
            is_external = bool(job_obj.is_external)
            source_portal = job_obj.source_portal
            source_url = job_obj.source_url
    elif opp_type == 'scholarship':
        sch_obj = Scholarship.objects.filter(id=opp_id).first()
        if sch_obj:
            opp_name = opp_name or sch_obj.name
            org = org or sch_obj.provider
            is_external = bool(sch_obj.is_external)
            source_portal = sch_obj.source_portal
            source_url = sch_obj.source_url
    elif opp_type == 'scheme':
        scm_obj = GovernmentScheme.objects.filter(id=opp_id).first()
        if scm_obj:
            opp_name = opp_name or scm_obj.name
            org = org or scm_obj.department
            is_external = bool(scm_obj.is_external)
            source_portal = scm_obj.source_portal
            source_url = scm_obj.source_url
    elif opp_type == 'skill':
        skl_obj = SkillProgram.objects.filter(id=opp_id).first()
        if skl_obj:
            opp_name = opp_name or skl_obj.name
            org = org or skl_obj.provider
            is_external = bool(skl_obj.is_external)
            source_portal = skl_obj.source_portal
            source_url = skl_obj.source_url
    elif opp_type == 'business':
        biz_obj = BusinessOpportunity.objects.filter(id=opp_id).first()
        if biz_obj:
            opp_name = opp_name or biz_obj.name
            org = org or 'Micro-Enterprise Track'
            is_external = bool(biz_obj.is_external)
            source_portal = biz_obj.source_portal
            source_url = biz_obj.source_url

    if not opp_name:
        opp_name = f"Opportunity #{opp_id}"

    # Flow 2 Enforcement: External opportunities require applying on the official portal!
    if is_external:
        return JsonResponse({
            'status': 'external_portal',
            'is_external': True,
            'source_portal': source_portal or 'Official Portal',
            'source_url': source_url or '#',
            'message': f'Application for "{opp_name}" is handled directly by the official {source_portal or "external"} portal.',
            'opportunity_name': opp_name
        })

    # Flow 1: Internal application resolution
    applicant_name = (request.POST.get('applicant_name') or request.POST.get('guest_name') or '').strip()
    applicant_phone = (request.POST.get('applicant_phone') or request.POST.get('phone') or '').strip()
    applicant_location = (request.POST.get('applicant_location') or request.POST.get('location') or '').strip()
    cover_note = (request.POST.get('cover_note') or '').strip()

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    else:
        full_name = applicant_name or 'Guest Candidate'
        first_name = full_name.split()[0] if full_name else 'Guest'
        last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else 'Applicant'
        guest_email = (request.POST.get('applicant_email') or 'guest@ruralopportunity.org').strip()
        guest_user, _ = User.objects.get_or_create(
            username='guest_candidate',
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': guest_email
            }
        )
        profile, _ = UserProfile.objects.get_or_create(user=guest_user)

    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('Accept', '') or
        request.POST.get('is_ajax') == '1'
    )

    # Check for duplicate application
    existing_app = Application.objects.filter(
        user=profile,
        opportunity_type=opp_type,
        opportunity_id=opp_id
    ).first()

    total_active = Application.objects.filter(user=profile).count()

    if existing_app:
        if is_ajax:
            return JsonResponse({
                'status': 'already_applied',
                'already_applied': True,
                'message': f'You have already applied for "{existing_app.opportunity_name}".',
                'application_id': existing_app.id,
                'opportunity_name': existing_app.opportunity_name,
                'active_applications_count': total_active
            })
        messages.info(request, f'You have already applied for "{existing_app.opportunity_name}".')
        return redirect('applications' if request.user.is_authenticated else 'jobs_list')

    # Create verified application in database
    app = Application.objects.create(
        user=profile,
        opportunity_type=opp_type,
        opportunity_id=opp_id,
        opportunity_name=opp_name,
        organization=org,
        status='applied',
        applicant_phone=applicant_phone,
        applicant_location=applicant_location,
        cover_note=cover_note
    )

    # Track in guest session
    session_applied = request.session.get('applied_keys', [])
    key = f"{opp_type}_{opp_id}"
    if key not in session_applied:
        session_applied.append(key)
        request.session['applied_keys'] = session_applied

    updated_active = Application.objects.filter(user=profile).count()

    if is_ajax:
        return JsonResponse({
            'status': 'success',
            'already_applied': False,
            'message': f'Application for "{opp_name}" submitted successfully! 🎉',
            'application_id': app.id,
            'opportunity_name': opp_name,
            'active_applications_count': updated_active
        })

    messages.success(request, f'Application for "{opp_name}" submitted successfully! 🎉')
    return redirect('applications' if request.user.is_authenticated else 'jobs_list')
