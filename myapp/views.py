from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, ExperienceForm, RegistrationForm,LoginForm,ProfileForm,EducationForm

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('loginview')
    else:
        form = RegistrationForm()
    return render(request,'registration.html',{'form':form})

def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:

                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def logoutview(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('loginview')

@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:

        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

from .models import Education, Experience

@login_required
def dashboard(request):
    profile = get_profile(request.user)
    education_list = Education.objects.filter(profile=profile)
    experience_list = Experience.objects.filter(profile=profile)
    return render(request, 'dashboard.html', {
        'profile': profile,
        'education_list': education_list,
        'experience_list': experience_list,
    })

@login_required
def add_education(request):
    profile = get_profile(user=request.user)
    education_list = Education.objects.filter(profile=profile)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            messages.success(request, 'Education added successfully.')
            return redirect('dashboard')
    else:
        form = EducationForm()
    return render(request, 'add_education.html', {'form': form,'title': 'Add Education', 'education_list': education_list})

@login_required
def edit_education(request, pk):
    profile = get_profile(request.user)
    education = get_object_or_404(Education, pk=pk, profile=profile)
    education_list = Education.objects.filter(profile=profile)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education updated successfully.')
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education)

    return render(request, 'add_education.html', {
        'form': form,
        'title': 'Edit Education',
        'education_list': education_list,
        'editing': education,
    })
    
def delete_education(request, pk):
        profile = get_profile(request.user)
        education = get_object_or_404(Education, pk=pk, profile=profile)
        education.delete()
        messages.success(request, 'Education deleted successfully.')
        return redirect('dashboard')   
    
@login_required
def add_experience(request):
    profile = get_profile(request.user)
    experience_list = Experience.objects.filter(profile=profile)

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            messages.success(request, 'Experience added successfully.')
            return redirect('dashboard')
    else:
        form = ExperienceForm()

    return render(request, 'add_experience.html', {
        'form': form,
        'title': 'Add Experience',
        'experience_list': experience_list,
    })


@login_required
def edit_experience(request, pk):
    profile = get_profile(request.user)
    experience = get_object_or_404(Experience, pk=pk, profile=profile)   
    experience_list = Experience.objects.filter(profile=profile)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated successfully.')
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=experience)

    return render(request, 'add_experience.html', {
        'form': form,
        'title': 'Edit Experience',
        'experience_list': experience_list,
        'editing': experience,
    })


@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk, profile=get_profile(request.user))
    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Experience deleted.')
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'obj': experience})

@login_required
def resume(request):
    profile = get_profile(request.user)
    return render(request, 'resume.html', {
        'profile': profile,
        'education_list': Education.objects.filter(profile=profile),
        'experience_list': Experience.objects.filter(profile=profile),
        'skill_list': profile.skills.all(),
    })
    

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})







@login_required
def resume_pdf(request):
    profile = get_profile(request.user)

    html = render_to_string('resume_pdf.html', {
        'profile': profile,
        'education_list': Education.objects.filter(profile=profile),
        'experience_list': Experience.objects.filter(profile=profile),
        'skill_list': profile.skills.all(),
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'

    result = pisa.CreatePDF(html, dest=response)   
    if result.err:
        return HttpResponse('Could not generate the PDF.', status=500)
    return response