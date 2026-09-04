from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('saved-opportunities/', views.saved_opportunities, name='saved_opportunities'),
    path('applications/', views.application_tracker, name='applications'),
    path('documents/', views.document_checklist, name='document_checklist'),
    path('save-opportunity/', views.save_opportunity, name='save_opportunity'),
    path('about/', views.about_page, name='about'),
    path('partners/', views.partners_view, name='partners'),
    path('api/sync-partners/', views.sync_partners_api, name='sync_partners_api'),
]
