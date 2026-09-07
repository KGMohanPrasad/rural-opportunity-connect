from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Scholarship

def scholarship_list(request):
    """List scholarships"""
    scholarships = Scholarship.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        scholarships = scholarships.filter(Q(name__icontains=search) | Q(provider__icontains=search))
    
    education = request.GET.get('education', '')
    if education:
        scholarships = scholarships.filter(education_level=education)
    
    category = request.GET.get('category', '')
    if category:
        scholarships = scholarships.filter(category__icontains=category)
    
    context = {
        'scholarships': scholarships,
        'search': search,
        'filters': {
            'education': education,
            'category': category,
        }
    }
    return render(request, 'scholarships_list.html', context)

def scholarship_detail(request, scholarship_id):
    """View scholarship details"""
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    context = {'scholarship': scholarship}
    return render(request, 'scholarship_detail.html', context)
