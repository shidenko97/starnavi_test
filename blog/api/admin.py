from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.api.models import User


# Redeclare standard User model
admin.site.register(User, UserAdmin)
