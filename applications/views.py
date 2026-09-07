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

@csrf_exempt
def apply_opportunity(request):
    """
    Direct Quick Apply submission for both authenticated and guest candidates.
    Records application in database and prevents duplicates.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
        else:
            guest_name = (request.POST.get('guest_name') or 'Guest Applicant').strip()
            first_name = guest_name.split()[0] if guest_name else 'Guest'
            last_name = ' '.join(guest_name.split()[1:]) if len(guest_name.split()) > 1 else 'Applicant'
            guest_user, _ = User.objects.get_or_create(
                username='guest_candidate',
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': 'guest@ruralopportunity.org'
                }
            )
            profile, _ = UserProfile.objects.get_or_create(user=guest_user)
        opp_type = request.POST.get('opportunity_type') or 'job'
        try:
            opp_id = int(request.POST.get('opportunity_id') or 0)
        except (ValueError, TypeError):
            opp_id = 0

        opp_name = (request.POST.get('opportunity_name') or '').strip()
        org = (request.POST.get('organization') or '').strip()

        # Fallback to model lookup if name or org not provided in POST
        if (not opp_name or not org) and opp_id > 0:
            try:
                if opp_type == 'job':
                    job_obj = Job.objects.filter(id=opp_id).first()
                    if job_obj:
                        opp_name = opp_name or job_obj.title
                        org = org or job_obj.organization
                elif opp_type == 'scholarship':
                    sch_obj = Scholarship.objects.filter(id=opp_id).first()
                    if sch_obj:
                        opp_name = opp_name or sch_obj.name
                        org = org or sch_obj.provider
                elif opp_type == 'scheme':
                    scm_obj = GovernmentScheme.objects.filter(id=opp_id).first()
                    if scm_obj:
                        opp_name = opp_name or scm_obj.name
                        org = org or scm_obj.department
                elif opp_type == 'skill':
                    skl_obj = SkillProgram.objects.filter(id=opp_id).first()
                    if skl_obj:
                        opp_name = opp_name or skl_obj.name
                        org = org or skl_obj.provider
                elif opp_type == 'business':
                    biz_obj = BusinessOpportunity.objects.filter(id=opp_id).first()
                    if biz_obj:
                        opp_name = opp_name or biz_obj.name
                        org = org or 'Micro-Enterprise Track'
            except Exception:
                pass

        if not opp_name:
            opp_name = f"Opportunity #{opp_id}"

        # Check if already applied or create new
        app, created = Application.objects.get_or_create(
            user=profile,
            opportunity_type=opp_type,
            opportunity_id=opp_id,
            defaults={
                'opportunity_name': opp_name,
                'organization': org,
                'status': 'applied'
            }
        )

        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or
            'application/json' in request.headers.get('Accept', '') or
            request.POST.get('is_ajax') == '1'
        )

        if not created:
            if is_ajax:
                return JsonResponse({
                    'status': 'already_applied',
                    'already_applied': True,
                    'message': f'You have already applied for {app.opportunity_name}.',
                    'application_id': app.id,
                    'opportunity_name': app.opportunity_name
                })
            if request.user.is_authenticated:
                messages.info(request, f'You have already applied for "{app.opportunity_name}".')
                return redirect('applications')
            messages.info(request, f'You have already applied for "{app.opportunity_name}".')
            return redirect(request.META.get('HTTP_REFERER', 'jobs_list'))

        if is_ajax:
            return JsonResponse({
                'status': 'success',
                'already_applied': False,
                'message': f'Application for "{opp_name}" submitted successfully! 🎉',
                'application_id': app.id,
                'opportunity_name': opp_name
            })

        if request.user.is_authenticated:
            messages.success(request, f'Application for "{opp_name}" submitted successfully! 🎉')
            return redirect('applications')
        messages.success(request, f'Application for "{opp_name}" submitted successfully! 🎉')
        return redirect(request.META.get('HTTP_REFERER', 'jobs_list'))

    return JsonResponse({'status': 'error', 'message': 'Invalid request method. POST required.'}, status=400)
