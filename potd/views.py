from django.shortcuts import render
from .models import PhotoOfTheDay


def potd_day(request):
    context = {
        'photo': PhotoOfTheDay.objects.filter(feature_potd=True).order_by("-feature_potd").first()
    }
    return render(request, 'potd/potd_day.html', context)
