from django.contrib import messages
from django.conf import settings
from .forms import HomeEmailSignupForm
from django.shortcuts import redirect
from django.urls import reverse
from .models import Signup

import json
import requests

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'


def subscribe(email, first_name):
    data = {
        "email_address": email,
        "merge_fields": {
            "first_name": first_name
        },
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()


def home_list_signup(request):
    form = HomeEmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed ")
            else:
                print(form.instance)
                subscribe(form.instance.email, form.instance.first_name)
                form.save()
    return redirect(reverse('signup-thankyou'))



