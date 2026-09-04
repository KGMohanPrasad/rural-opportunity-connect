from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skills_list'),
    path('<int:skill_id>/', views.skill_detail, name='skill_detail'),
]
