from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='loginview'),
    path('logout/', views.logoutview, name='logoutview'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('education/add/', views.add_education, name='add_education'),
    path('education/edit/<int:pk>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:pk>/', views.delete_education, name='delete_education'),
    path('experience/add/', views.add_experience, name='add_experience'),
    path('experience/edit/<int:pk>/', views.edit_experience, name='edit_experience'),
    path('experience/delete/<int:pk>/', views.delete_experience, name='delete_experience'),
    path('resume/', views.resume, name='resume'),
    path('resume/download/', views.resume_pdf, name='resume_pdf'),
    path('contact/', views.contact, name='contact'),
]