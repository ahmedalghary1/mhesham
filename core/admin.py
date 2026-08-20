from django.contrib import admin
from .models import HomeContent, SiteSetting, Skill, SocialLink
admin.site.register([HomeContent, SiteSetting, Skill, SocialLink])
