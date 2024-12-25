from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import YamdbUser


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role', 'confirmation_code')}),
)

admin.site.register(YamdbUser, UserAdmin)