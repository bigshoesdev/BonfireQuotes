from django.contrib import admin
from bonfire_quotes.admin import admin_site
from .models import PhotoOfTheDay


class PhotoOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('title', 'photographer', 'feature_potd', 'featured_as_potd', 'featured_date', 'photographer_url')


admin_site.register(PhotoOfTheDay, PhotoOfTheDayAdmin)