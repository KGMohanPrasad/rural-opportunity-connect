from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='jobs_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
]
