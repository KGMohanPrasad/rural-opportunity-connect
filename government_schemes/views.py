from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import GovernmentScheme

def scheme_list(request):
    """List government schemes"""
    schemes = GovernmentScheme.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        schemes = schemes.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    category = request.GET.get('category', '')
    if category:
        schemes = schemes.filter(category=category)
    
    context = {
        'schemes': schemes,
        'search': search,
        'categories': GovernmentScheme._meta.get_field('category').choices,
        'filters': {
            'category': category,
        }
    }
    return render(request, 'schemes_list.html', context)

def scheme_detail(request, scheme_id):
    """View scheme details"""
    scheme = get_object_or_404(GovernmentScheme, id=scheme_id)
    context = {'scheme': scheme}
    return render(request, 'scheme_detail.html', context)
