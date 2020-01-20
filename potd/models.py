from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from slugger import AutoSlugField


class PhotoOfTheDay(models.Model):
    title = models.CharField(max_length=100, default="")
    photographer = models.CharField(max_length=100, default="")
    img = models.ImageField(default='potd_default.jpg', upload_to='potd')
    photographer_url = models.URLField(max_length=100, default="", verbose_name="Photographer url")

    slug = AutoSlugField(populate_from='title')
    draft = models.BooleanField(default=False)

    published = models.DateTimeField(default=timezone.now, auto_now=False, auto_now_add=False)
    date_posted = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    feature_potd = models.BooleanField(default=False, verbose_name="Featured POTD")
    featured_as_potd = models.BooleanField(default=False, verbose_name="Has Been POTD")
    featured_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_featured_date(self):
        if self.featured_date:
            return True
        else:
            return False


    class Meta:
        verbose_name_plural = "Photo of the day"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(PhotoOfTheDay, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

    


