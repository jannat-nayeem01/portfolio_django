from django.db import models

from django.contrib.auth.models import AbstractUser

from core import settings

class CustomUser(AbstractUser):
        def __str__(self):
            return self.username


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='profiles')
    experience = models.TextField(blank=True)
    extracurricular_activities = models.TextField(blank=True)
    career_objectives = models.TextField(blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    degree_choices = [
        ('SSC','SSC'),
        ('HSC','HSC'),
        ('Diploma','Diploma'),
        ('Bachelors','Bachelors'),
        ('Masters','Masters'),
        ('PhD','PhD'),
        ('Other','Other'),
    ]
    degree = models.CharField(max_length=100, choices=degree_choices)
    institution = models.CharField(max_length=200)
    passing_year = models.PositiveIntegerField()
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-passing_year']

    def __str__(self):
        return f"{self.degree} from {self.institution}"
class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company}"
class Project(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name = 'projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    github_link = models.URLField(blank=True)
    live_demo_link = models.URLField(blank=True)
    technologies_used = models.ManyToManyField(Skill, blank=True, related_name='projects')
    
    def __str__(self):
        return self.title
    
class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    class Meta:
        ordering = ['-issue_date']
    def __str__(self):
        return f"{self.title} from {self.issuing_organization}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
