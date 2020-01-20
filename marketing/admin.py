from django.contrib import admin
from bonfire_quotes.admin import admin_site
from .models import Signup


class SignupsAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')


admin_site.register(Signup, SignupsAdmin)