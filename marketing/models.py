from django.db import models


class Signup(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=50, default="", verbose_name="First")
    last_name = models.CharField(max_length=50, default="", verbose_name="Last")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

