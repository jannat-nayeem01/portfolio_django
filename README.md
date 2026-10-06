# portfolio-project

A Django career portfolio app. Users register, log in, manage their profile (education, experience, skills) from a dashboard, and view or download their CV.


## Models

| Model | Relationship | Purpose |
|---|---|---|
| `CustomUser` | extends `AbstractUser` | login and registration |
| `Profile` | one-to-one with `CustomUser` | basic info (name, contact, bio, links, addresses) |
| `Education` | many-to-one with `Profile` | degree, institution, passing year, GPA |
| `Experience` | many-to-one with `Profile` | job title, company, dates, description |
| `Skill` | many-to-many with `Profile` | shared pool of skill names |
| `ContactMessage` | standalone | messages sent through the contact form |

## 1. Local Setup & Package Installs

Check the Python version, create a virtual environment, and install Django.

```bash
python3 --version

python3 -m venv venv              # on Windows: python -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate

pip install django
python -m django --version
```

## 2. Start Project and App

```bash
django-admin startproject portfolioproject .
django-admin startapp portfolio

git init
```

Create a `.gitignore` with at least:

```
venv/
__pycache__/
*.pyc
db.sqlite3
media/
.env
```

## 3. Register the App and Set the Custom User (before the first migrate)

Set this up **before** running any migration. Changing `AUTH_USER_MODEL` after the first `migrate` breaks the migration history, and the usual fix is deleting the database.

1. Define `CustomUser` in `portfolio/models.py`:

```python
   from django.contrib.auth.models import AbstractUser

   class CustomUser(AbstractUser):
       pass
```

2. Open `portfolioproject/settings.py`:

```python
   INSTALLED_APPS = [
       ...
       'portfolio',
   ]

   AUTH_USER_MODEL = 'portfolio.CustomUser'

   LOGIN_URL = 'login'
   LOGIN_REDIRECT_URL = 'dashboard'
   LOGOUT_REDIRECT_URL = 'login'
```

3. Map the `error` message tag to Bootstrap's `danger` class so error alerts get a color:

```python
   from django.contrib.messages import constants as message_constants

   MESSAGE_TAGS = {
       message_constants.ERROR: 'danger',
   }
```

## 4. URLs

### Main URLs (`portfolioproject/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
]
```

### App URLs (`portfolio/urls.py`)

Create this file manually in the app folder.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('education/add/', views.add_education, name='add_education'),
    path('education/<int:pk>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:pk>/delete/', views.delete_education, name='delete_education'),

    path('experience/add/', views.add_experience, name='add_experience'),
    path('experience/<int:pk>/edit/', views.edit_experience, name='edit_experience'),
    path('experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),

    path('resume/', views.resume, name='resume'),
    path('resume/pdf/', views.resume_pdf, name='resume_pdf'),

    path('contact/', views.contact, name='contact'),
    # plus your register / login / logout routes
]
```

## 5. Models, Forms and Admin Workflow

1. Add the remaining models to `portfolio/models.py`: `Skill`, `Profile`, `Education`, `Experience`, `ContactMessage`.
2. Create `portfolio/forms.py` for `RegistrationForm`, `LoginForm`, `ProfileForm`, `EducationForm`, `ExperienceForm` and `ContactForm`.
3. Create the template folders and files:

```
   portfolio/templates/
   ├── base.html                 # navbar, messages block, Bootstrap CDN
   ├── dashboard.html
   ├── edit_profile.html
   ├── add_education.html
   ├── add_experience.html
   ├── _education_list.html      # reusable partial
   ├── _experience_list.html     # reusable partial
   ├── confirm_delete.html
   ├── resume.html
   ├── resume_pdf.html           # only if using server-side PDF
   ├── contact.html
   ├── login.html
   └── register.html
```

4. Register the models in `portfolio/admin.py`:

```python
   from django.contrib import admin
   from .models import (
       CustomUser, Profile, Education, Experience, Skill, ContactMessage,
   )






   admin.site.register(CustomUser)
   admin.site.register(Skill)
   admin.site.register(ContactMessage)
```

## 6. Migrations & Superuser

Now that the custom user and all models exist, create the database.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Choose your own username and a strong password. Do not commit credentials to the repository.

After the first run, open `/admin/` and add a few skills (Python, Django, SQL, HTML, CSS, Git), because the profile form shows only skills that already exist.

When a model changes later, run the same two commands again:

```bash
python manage.py makemigrations
python manage.py migrate
```

If Django asks whether a field was renamed (for example `cgpa` to `gpa`), answer `y` to keep the existing data.

## 7. PDF Generation (Optional)

Two ways to produce a PDF of the CV:

* **Browser print:** the CV page has a Print / Save as PDF button (`window.print()`) and `@media print` CSS. No extra package needed.
* **Server-side download:** uses `xhtml2pdf`.

```bash
  pip install xhtml2pdf
```



## 9. Run Server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in. Useful pages:

| Page | URL |
|---|---|
| Dashboard | `/dashboard/` |
| Edit profile | `/profile/edit/` |
| CV | `/resume/` |
| CV as PDF | `/resume/pdf/` |
| Contact | `/contact/` |
| Admin | `/admin/` |

## Dependencies

Freeze installed packages any time you add a new one, and keep the file committed:

```bash
pip freeze > requirements.txt
```

Rebuild the environment elsewhere:

```bash
pip install -r requirements.txt
```

## Git

```bash
git config --list
git remote -v
git status
git add .
git commit -m "Describe your change"
```