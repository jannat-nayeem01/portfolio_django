from .models import *
import django.forms as forms

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        })
    )
    field_order = ['username', 'email', 'password', 'confirm_password']

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','contact_number',
                  'linkedin_profile', 'github_profile',
                  'present_address', 'permanent_address', 
                  'skills', 'experience', 'extracurricular_activities', 
                  'career_objectives', 'expected_salary', 'bio', 'location', 'birth_date']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'present_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'extracurricular_activities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'career_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'expected_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }
        
class EducationForm(forms.ModelForm):
    degree_choices = [
        ('', 'Select Degree'),
        ('SSC','SSC'),
        ('HSC','HSC'),
        ('Diploma','Diploma'),
        ('Bachelors','Bachelors'),
        ('Masters','Masters'),  
        ('PhD','PhD'),
        ('Other','Other'),
    ]
    degree = forms.ChoiceField(choices=degree_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    passing_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gpa = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'passing_year', 'gpa']
        
from django import forms
from .models import Experience


class ExperienceForm(forms.ModelForm):
    job_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    company = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
