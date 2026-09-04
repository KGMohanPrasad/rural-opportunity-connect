from django.shortcuts import render
from django.db.models import Q
from .models import SkillProgram

def skill_list(request):
    """List skill programs"""
    skills = SkillProgram.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        skills = skills.filter(Q(name__icontains=search) | Q(category__icontains=search))
    
    category = request.GET.get('category', '')
    if category:
        skills = skills.filter(category__icontains=category)
    
    level = request.GET.get('level', '')
    if level:
        skills = skills.filter(level=level)
    
    price_type = request.GET.get('price_type', '') or request.GET.get('price', '')
    if price_type:
        skills = skills.filter(price_type=price_type)
    
    context = {
        'skills': skills,
        'search': search,
        'filters': {
            'category': category,
            'level': level,
            'price_type': price_type,
        }
    }
    return render(request, 'skills_list.html', context)

def skill_detail(request, skill_id):
    """View skill details"""
    skill = SkillProgram.objects.get(id=skill_id)
    context = {'skill': skill}
    return render(request, 'skill_detail.html', context)
