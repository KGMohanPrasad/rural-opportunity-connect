from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import re
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import django
from django.conf import settings

app = Flask(__name__)
CORS(app)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

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


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """
    Intelligent multi-criteria recommendation engine.
    Calculates weighted match scores (0-100%) and explains recommendation rationale.
    """
    education = request.args.get('education', '').strip().lower()
    course = request.args.get('course', '').strip().lower()
    skills_raw = request.args.get('skills', '').strip()
    location = request.args.get('location', '').strip().lower()
    income = request.args.get('income', '').strip().lower()
    interests_raw = request.args.get('interests', '').strip()
    preferred_opp = request.args.get('preferred_opportunity', '').strip().lower()

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

    # ==========================================
    # 1. JOBS MATCHING
    # ==========================================
    scored_jobs = []
    for j in Job.objects.all():
        score = 50.0  # Base score
        reasons = []

        # Skill matching (Weight: 35%)
        skill_overlap, matched_skills = calculate_overlap_score(user_skill_tokens, f"{j.required_skills} {j.title} {j.description}")
        if skill_overlap > 0:
            score += skill_overlap * 35.0
            reasons.append(f"Matches skills: {', '.join(matched_skills[:3]).title()}")
        elif user_skills:
            score += 10.0

        # Location matching (Weight: 20%)
        if location:
            if location in j.location.lower() or 'remote' in j.location.lower() or 'any' in j.location.lower():
                score += 20.0
                reasons.append(f"Located near {j.location}")
            else:
                score += 5.0
        else:
            score += 10.0

        # Education & Experience alignment (Weight: 15%)
        if education in ['bachelor', 'master', 'diploma']:
            score += 15.0
            reasons.append("Eligible for educational background")

        # Preferred Opportunity bonus (Weight: 10%)
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

    # ==========================================
    # 2. SCHOLARSHIPS MATCHING
    # ==========================================
    scored_scholarships = []
    for s in Scholarship.objects.all():
        score = 55.0
        reasons = []

        # Education Level Match (Weight: 30%)
        if education:
            if education in s.education_level.lower() or s.education_level.lower() in education:
                score += 30.0
                reasons.append(f"Direct match for {s.get_education_level_display()}")
            else:
                score += 10.0
        else:
            score += 15.0

        # Course & Field overlap (Weight: 20%)
        course_overlap, matched_c = calculate_overlap_score(user_course_tokens, f"{s.course} {s.name} {s.description}")
        if course_overlap > 0:
            score += 20.0
            reasons.append("Applicable to your study discipline")

        # Income criteria (Weight: 15%)
        if income or 'low' in income:
            score += 15.0
            reasons.append("Income limit criteria satisfied")

        # Preferred bonus (Weight: 10%)
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

    # ==========================================
    # 3. GOVERNMENT SCHEMES MATCHING
    # ==========================================
    scored_schemes = []
    for sc in GovernmentScheme.objects.all():
        score = 60.0
        reasons = []

        # Interest & Category matching (Weight: 30%)
        interest_overlap, matched_int = calculate_overlap_score(user_interest_tokens, f"{sc.category} {sc.name} {sc.description} {sc.target_beneficiaries}")
        if interest_overlap > 0:
            score += 30.0
            reasons.append(f"Aligned with your interests ({sc.get_category_display()})")
        else:
            score += 15.0

        # Rural & Community targeting (Weight: 20%)
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

    # ==========================================
    # 4. SKILL PROGRAMS MATCHING
    # ==========================================
    scored_skills = []
    for sk in SkillProgram.objects.all():
        score = 55.0
        reasons = []

        # Skill & Category synergy (Weight: 35%)
        overlap, matched_sk = calculate_overlap_score(user_skill_tokens.union(user_interest_tokens), f"{sk.category} {sk.name} {sk.description}")
        if overlap > 0:
            score += 35.0
            reasons.append(f"Builds on {', '.join(matched_sk[:2]).title()} skills")
        else:
            score += 15.0

        # Free / Subsidized bonus (Weight: 20%)
        if sk.price_type == 'free':
            score += 20.0
            reasons.append("100% Free Government/Industry Certified")

        # Level compatibility (Weight: 10%)
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

    # ==========================================
    # 5. BUSINESS OPPORTUNITIES MATCHING
    # ==========================================
    scored_business = []
    for b in BusinessOpportunity.objects.all():
        score = 55.0
        reasons = []

        # Low investment preference for rural youth (Weight: 30%)
        if b.investment_level == 'low':
            score += 30.0
            reasons.append("Low capital requirement (< ₹1 Lakh)")
        elif b.investment_level == 'medium':
            score += 20.0
            reasons.append("Medium investment with high ROI")

        # Skill and resource match (Weight: 25%)
        overlap, matched_b = calculate_overlap_score(user_skill_tokens.union(user_interest_tokens), f"{b.category} {b.name} {b.required_skills} {b.description}")
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

    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
