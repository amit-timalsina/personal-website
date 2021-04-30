from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from .models import *

# Create your views here.

def home(request):
    return render(request, 'base/index.html')

def contact(request):
    return render(request, 'base/contact.html')

def profile(request):
    return(request, 'base/profile.html')

def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('base/email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
    
    email = EmailMessage(
        request.POST['subject'],
        template,
        settings.EMAIL_HOST_USER,
        ['amittimalsina14@gmail.com']
    )

    email.fail_silently = False
    email.send()
    
    return render(request, 'base/email_sent.html')

def about(request):
    return render(request, 'base/about.html')

def registerPage(request):
    return render(request, 'base/post_form.html')