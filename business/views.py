from django.shortcuts import render
from django.db.models import Q
from .models import BusinessOpportunity

def business_list(request):
    """List business opportunities"""
    businesses = BusinessOpportunity.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        businesses = businesses.filter(Q(name__icontains=search) | Q(category__icontains=search))
    
    category = request.GET.get('category', '')
    if category:
        businesses = businesses.filter(category__icontains=category)
    
    investment = request.GET.get('investment', '')
    if investment:
        businesses = businesses.filter(investment_level=investment)
    
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        businesses = businesses.filter(opportunity_level=difficulty)
    
    context = {
        'businesses': businesses,
        'business_ideas': businesses,
        'search': search,
        'filters': {
            'category': category,
            'investment': investment,
            'difficulty': difficulty,
        }
    }
    return render(request, 'business_list.html', context)

def business_detail(request, business_id):
    """View business details"""
    business = BusinessOpportunity.objects.get(id=business_id)
    context = {'business': business}
    return render(request, 'business_detail.html', context)
