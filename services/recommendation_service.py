"""
Rural Opportunity Connect - Recommendation Service
Provides personalized, multi-criteria recommendation scoring for rural citizens.
Works seamlessly via Flask microservice (port 5000) or directly within Django.
"""

import re
import requests
from django.conf import settings
from opportunities.models import Job
from scholarships.models import Scholarship
from government_schemes.models import GovernmentScheme
from skills.models import SkillProgram
from business.models import BusinessOpportunity

def tokenize(text):
    """Clean and split text into normalized tokens"""
    if not text:
        return set()
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', str(text).lower())
    return {word.strip() for word in cleaned.split() if len(word.strip()) > 2}

def calculate_overlap_score(user_tokens, target_text):
    """Compute token overlap ratio with target text"""
    if not user_tokens or not target_text:
        return 0.0, []
    target_tokens = tokenize(target_text)
    matched = user_tokens.intersection(target_tokens)
    if not matched:
        return 0.0, []
    score = min(1.0, len(matched) / max(1, len(user_tokens)))
    return score, list(matched)

class RecommendationService:
    @staticmethod
    def get_recommendations(profile):
        """
        Fetch recommendations from Flask microservice if running,
        or compute intelligent multi-criteria scores locally in Django.
        """
        api_url = getattr(settings, 'RECOMMENDATION_API_URL', 'http://localhost:5000/api/recommendations')
        try:
            res = requests.get(
                api_url,
                params={
                    'education': profile.education or '',
                    'course': profile.course or '',
                    'skills': profile.skills or '',
                    'location': profile.location or '',
                    'income': profile.annual_income or '',
                    'interests': profile.interests or '',
                    'preferred_opportunity': profile.preferred_opportunity or '',
                },
                timeout=1.5
            )
            if res.status_code == 200:
                data = res.json()
                if any(data.get(k) for k in ('jobs', 'scholarships', 'schemes', 'skills', 'business')):
                    return data
        except Exception:
            pass

        # Internal fallback scoring algorithm
        return RecommendationService.compute_local_recommendations(profile)

    @staticmethod
    def compute_local_recommendations(profile):
        education = (profile.education or '').strip().lower()
        course = (profile.course or '').strip().lower()
        skills_raw = profile.skills or ''
        location = (profile.location or '').strip().lower()
        income = (profile.annual_income or '').strip().lower()
        interests_raw = profile.interests or ''
        preferred_opp = (profile.preferred_opportunity or '').strip().lower()

        user_skills = {s.strip().lower() for s in skills_raw.split(',') if s.strip()} if skills_raw else set()
        user_skill_tokens = tokenize(skills_raw)
        user_interest_tokens = tokenize(interests_raw)
        user_course_tokens = tokenize(course)

        recommendations = {
            'jobs': [],
            'scholarships': [],
            'schemes': [],
            'skills': [],
            'business': []
        }

        # 1. Jobs Matching
        scored_jobs = []
        for j in Job.objects.all():
            score = 50.0
            reasons = []

            skill_overlap, matched_skills = calculate_overlap_score(user_skill_tokens, f"{j.required_skills} {j.title} {j.description}")
            if skill_overlap > 0:
                score += skill_overlap * 35.0
                reasons.append(f"Matches skills: {', '.join(matched_skills[:3]).title()}")
            elif user_skills:
                score += 10.0

            if location:
                if location in j.location.lower() or 'remote' in j.location.lower() or 'any' in j.location.lower():
                    score += 20.0
                    reasons.append(f"Located near {j.location}")
                else:
                    score += 5.0
            else:
                score += 10.0

            if education in ['bachelor', 'master', 'diploma']:
                score += 15.0
                reasons.append("Eligible for educational background")

            if preferred_opp in ['jobs', '']:
                score += 10.0

            if not reasons:
                reasons.append("High rural growth sector opportunity")

            final_score = int(min(99, max(60, score)))
            scored_jobs.append({
                'id': j.id,
                'title': j.title,
                'organization': j.organization,
                'location': j.location,
                'salary_min': j.salary_min,
                'salary_max': j.salary_max,
                'job_type': j.get_job_type_display(),
                'required_skills': j.required_skills,
                'match_score': final_score,
                'match_reasons': reasons[:3]
            })

        scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        recommendations['jobs'] = scored_jobs[:4]

        # 2. Scholarships Matching
        scored_scholarships = []
        for s in Scholarship.objects.all():
            score = 55.0
            reasons = []

            if education:
                if education in s.education_level.lower() or s.education_level.lower() in education:
                    score += 30.0
                    reasons.append(f"Direct match for {s.get_education_level_display()}")
                else:
                    score += 10.0
            else:
                score += 15.0

            course_overlap, _ = calculate_overlap_score(user_course_tokens, f"{s.course} {s.name} {s.description}")
            if course_overlap > 0:
                score += 20.0
                reasons.append("Applicable to your study discipline")

            if income or 'low' in income:
                score += 15.0
                reasons.append("Income limit criteria satisfied")

            if preferred_opp in ['scholarships', '']:
                score += 10.0

            if not reasons:
                reasons.append("Full financial aid & educational grant")

            final_score = int(min(99, max(65, score)))
            scored_scholarships.append({
                'id': s.id,
                'name': s.name,
                'provider': s.provider,
                'amount': s.amount,
                'education_level': s.get_education_level_display(),
                'income_limit': s.income_limit,
                'match_score': final_score,
                'match_reasons': reasons[:3]
            })

        scored_scholarships.sort(key=lambda x: x['match_score'], reverse=True)
        recommendations['scholarships'] = scored_scholarships[:4]

        # 3. Government Schemes Matching
        scored_schemes = []
        for sc in GovernmentScheme.objects.all():
            score = 60.0
            reasons = []

            interest_overlap, _ = calculate_overlap_score(user_interest_tokens, f"{sc.category} {sc.name} {sc.description} {sc.target_beneficiaries}")
            if interest_overlap > 0:
                score += 30.0
                reasons.append(f"Aligned with your interests ({sc.get_category_display()})")
            else:
                score += 15.0

            if 'rural' in sc.category.lower() or 'agriculture' in sc.category.lower() or 'financial' in sc.category.lower():
                score += 20.0
                reasons.append("Direct rural & livelihood welfare subsidy")

            if not reasons:
                reasons.append("Government subsidy with direct benefit transfer")

            final_score = int(min(99, max(70, score)))
            scored_schemes.append({
                'id': sc.id,
                'name': sc.name,
                'department': sc.department,
                'category': sc.get_category_display(),
                'benefits': sc.benefits[:120] + '...' if len(sc.benefits) > 120 else sc.benefits,
                'match_score': final_score,
                'match_reasons': reasons[:3]
            })

        scored_schemes.sort(key=lambda x: x['match_score'], reverse=True)
        recommendations['schemes'] = scored_schemes[:4]

        # 4. Skill Programs Matching
        scored_skills = []
        for sk in SkillProgram.objects.all():
            score = 55.0
            reasons = []

            overlap, matched_sk = calculate_overlap_score(user_skill_tokens.union(user_interest_tokens), f"{sk.category} {sk.name} {sk.description}")
            if overlap > 0:
                score += 35.0
                reasons.append(f"Builds on {', '.join(matched_sk[:2]).title()} skills")
            else:
                score += 15.0

            if sk.price_type == 'free':
                score += 20.0
                reasons.append("100% Free Government/Industry Certified")

            if sk.level in ['beginner', 'intermediate']:
                score += 10.0
                reasons.append("Beginner friendly with practical training")

            final_score = int(min(99, max(65, score)))
            scored_skills.append({
                'id': sk.id,
                'name': sk.name,
                'category': sk.category,
                'duration': sk.duration,
                'level': sk.get_level_display(),
                'price_type': sk.get_price_type_display(),
                'certificate': sk.certificate,
                'match_score': final_score,
                'match_reasons': reasons[:3]
            })

        scored_skills.sort(key=lambda x: x['match_score'], reverse=True)
        recommendations['skills'] = scored_skills[:4]

        # 5. Business Opportunities Matching
        scored_business = []
        for b in BusinessOpportunity.objects.all():
            score = 55.0
            reasons = []

            if b.investment_level == 'low':
                score += 30.0
                reasons.append("Low capital requirement (< ₹1 Lakh)")
            elif b.investment_level == 'medium':
                score += 20.0
                reasons.append("Medium investment with high ROI")

            overlap, _ = calculate_overlap_score(user_skill_tokens.union(user_interest_tokens), f"{b.category} {b.name} {b.required_skills} {b.description}")
            if overlap > 0:
                score += 25.0
                reasons.append(f"Fits your {b.category} domain knowledge")

            if not reasons:
                reasons.append("High rural market demand & local scalability")

            final_score = int(min(99, max(65, score)))
            scored_business.append({
                'id': b.id,
                'name': b.name,
                'category': b.category,
                'investment_level': b.get_investment_level_display(),
                'opportunity_level': b.get_opportunity_level_display(),
                'expected_income': b.expected_income,
                'match_score': final_score,
                'match_reasons': reasons[:3]
            })

        scored_business.sort(key=lambda x: x['match_score'], reverse=True)
        recommendations['business'] = scored_business[:4]

        return recommendations
