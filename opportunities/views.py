from django.shortcuts import render
from django.db.models import Q
from .models import Job
from accounts.models import UserProfile

def job_list(request):
    """List all jobs with filters and search"""
    jobs = Job.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(organization__icontains=search) | Q(description__icontains=search))
    
    # Filters
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    experience = request.GET.get('experience', '')
    if experience:
        jobs = jobs.filter(experience_required__icontains=experience)
    
    salary_min = request.GET.get('salary_min', '')
    if salary_min:
        jobs = jobs.filter(salary_min__gte=int(salary_min))
    
    salary_max = request.GET.get('salary_max', '')
    if salary_max:
        jobs = jobs.filter(salary_max__lte=int(salary_max))
    
    context = {
        'jobs': jobs,
        'search': search,
        'filters': {
            'location': location,
            'job_type': job_type,
            'experience': experience,
            'salary_min': salary_min,
            'salary_max': salary_max,
        }
    }
    return render(request, 'jobs_list.html', context)

def job_detail(request, job_id):
    """View job details"""
    job = Job.objects.get(id=job_id)
    context = {
        'job': job,
        'skills_list': job.required_skills.split(',')
    }
    return render(request, 'job_detail.html', context)
