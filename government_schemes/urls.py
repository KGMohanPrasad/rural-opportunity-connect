from django.urls import path
from . import views

urlpatterns = [
    path('', views.scheme_list, name='schemes_list'),
    path('<int:scheme_id>/', views.scheme_detail, name='scheme_detail'),
]
