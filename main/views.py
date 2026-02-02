from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import (
    Profile, Skill, Project, Experience, 
    Education, Certification, Testimonial
)
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def index(request):
    profile = Profile.objects.first()
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    skills = Skill.objects.all()
    education = Education.objects.all()[:2] 
    certifications = Certification.objects.all()[:3] 
    testimonials = Testimonial.objects.all()[:3]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'skills': skills,
        'education': education,
        'certifications': certifications,
        'testimonials': testimonials,
    }
    return render(request, 'index.html', context)

def about(request):
    profile = Profile.objects.first()
    experiences = Experience.objects.all()
    education = Education.objects.all()
    certifications = Certification.objects.all()
    
    context = {
        'profile': profile,
        'experiences': experiences,
        'education': education,
        'certifications': certifications,
    }
    return render(request, 'about.html', context)

def projects(request):
    all_projects = Project.objects.all()
    
    context = {
        'projects': all_projects,
    }
    return render(request, 'projects.html', context)

def skills(request):
    frontend_skills = Skill.objects.filter(category='frontend')
    backend_skills = Skill.objects.filter(category='backend')
    database_skills = Skill.objects.filter(category='database')
    tools_skills = Skill.objects.filter(category='tools')
    
    context = {
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'database_skills': database_skills,
        'tools_skills': tools_skills,
    }
    return render(request, 'skills.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save()

            name = contact.name
            email = contact.email
            message = contact.message

            subject = f"New Contact Message from {name}"

            body = f"""
            You have received a new message from your website.
            Name: {name}
            Email: {email}
            Message:{message}
            """

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            messages.success(
                request,
                "Thank you! Your message has been sent successfully."
            )

            return redirect('contact')

    else:
        form = ContactForm()

    profile = Profile.objects.first()

    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, 'contact.html', context)