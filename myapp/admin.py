from django.contrib import admin

from .models import CustomUser, Profile, Skill, Education, Experience,Project,Certification,ContactMessage

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Project)        
admin.site.register(Certification)
admin.site.register(ContactMessage)