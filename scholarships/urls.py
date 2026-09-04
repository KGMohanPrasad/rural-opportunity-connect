from django.urls import path
from . import views

urlpatterns = [
    path('', views.scholarship_list, name='scholarships_list'),
    path('<int:scholarship_id>/', views.scholarship_detail, name='scholarship_detail'),
]
