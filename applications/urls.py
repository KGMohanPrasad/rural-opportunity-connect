from django.urls import path
from . import views

urlpatterns = [
    path('details/', views.get_opportunity_details, name='opportunity_details'),
    path('apply/', views.apply_opportunity, name='apply_opportunity'),
]
