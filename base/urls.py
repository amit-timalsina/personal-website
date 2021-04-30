from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('send_email/', views.sendEmail, name='send_email'),
    path('register/', views.registerPage, name='register')
]