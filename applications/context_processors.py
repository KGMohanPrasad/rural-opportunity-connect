from accounts.models import UserProfile
from applications.models import Application
from opportunities.models import SavedOpportunity

def user_opportunity_status(request):
    """
    Global context processor to inject sets of applied and saved opportunity keys.
    Format: 'job_1', 'scholarship_5', 'scheme_2', 'skill_3', 'business_4'
    Allows O(1) checks in all templates: e.g., 'job_'|add:job.id in user_applied_keys
    """
    if not request.user.is_authenticated:
        return {
            'user_applied_keys': set(),
            'user_saved_keys': set(),
        }

    try:
        profile = UserProfile.objects.filter(user=request.user).first()
        if not profile:
            return {
                'user_applied_keys': set(),
                'user_saved_keys': set(),
            }

        applied_tuples = Application.objects.filter(user=profile).values_list('opportunity_type', 'opportunity_id')
        applied_keys = {f"{opp_type}_{opp_id}" for opp_type, opp_id in applied_tuples}

        saved_tuples = SavedOpportunity.objects.filter(user=profile).values_list('opportunity_type', 'opportunity_id')
        saved_keys = {f"{opp_type}_{opp_id}" for opp_type, opp_id in saved_tuples}

        return {
            'user_applied_keys': applied_keys,
            'user_saved_keys': saved_keys,
        }
    except Exception:
        return {
            'user_applied_keys': set(),
            'user_saved_keys': set(),
        }
