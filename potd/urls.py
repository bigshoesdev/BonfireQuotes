from django.urls import path
from . import views

urlpatterns = [
    path('photo-of-the-day', views.potd_day, name="potd-day"),
]
