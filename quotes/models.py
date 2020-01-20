from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Background(models.Model):
    color = models.CharField(max_length=100, default="")
    slug = models.SlugField(unique=True, default="")

    def __str__(self):
        return self.color


class Post(models.Model):
    quote = models.CharField(max_length=200, default="")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)

    categories = models.ManyToManyField('Category', through='PostCategory')
    backgrounds = models.ManyToManyField('Background', through='PostBackground')

    draft = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)

    published = models.DateTimeField(default=timezone.now, auto_now=False, auto_now_add=False)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    likes = models.IntegerField(default=0)
    
    feature_qotd = models.BooleanField(default=False, verbose_name="Featured QOTD")
    featured_as_qotd = models.BooleanField(default=False, verbose_name="Has Been QOTD")
    featured_date = models.DateTimeField(null=True, blank=True)

    img = models.ImageField(default='default.jpg', upload_to='quote_pics', verbose_name="Quote Img")
    img_author = models.CharField(max_length=50, default="", verbose_name="Photographer")
    img_author_url = models.URLField(max_length=100, default="", verbose_name="Photographer url")

    @property
    def is_featured_date(self):
        if self.featured_date:
            return True
        else:
            return False

    def __str__(self):
        return self.quote

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostForm(forms.Form):
    id = forms.CharField(max_length=100, widget=forms.HiddenInput(), required=False)
    quote = forms.CharField(label='Quote', max_length=100, min_length=10,
                            widget=forms.Textarea(attrs={'placeholder': '', 'rows': 4, 'class': 'form-control'}),
                            required=True)
    author = forms.CharField(label='Author', max_length=30,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
                             required=True)
    category1 = forms.CharField(label='Category 1 ', max_length=15,
                                widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
                                required=False)
    category2 = forms.CharField(label='Category 2 ', max_length=15,
                                widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
                                required=False)
    background1 = forms.CharField(label='Background 1 ', max_length=15,
                                  widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control colorpicker-anchor'}),
                                  required=True)
    background2 = forms.CharField(label='Background 2 ', max_length=15,
                                  widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control colorpicker-anchor'}),
                                  required=True)

    def clean(self):
        cleaned_data = super().clean()

        posts = Post.objects.filter(quote=slugify(cleaned_data['quote'], allow_unicode=True))

        if len(posts) > 0:
            raise forms.ValidationError("The post that has same quote has already existed.")

        cate1 = cleaned_data.get("category1")
        cate2 = cleaned_data.get("category2")

        background1 = cleaned_data.get("background1")
        background2 = cleaned_data.get("background2")

        if cate1 == "" and cate2 == "":
            raise forms.ValidationError("You have to input at least one category.")

        if cate1 == cate2:
            raise forms.ValidationError("The categories should be different.")

        if background1 == background2:
            raise forms.ValidationError("The backgrounds should be different.")


class PostBackground(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)


class PostCategory(models.Model):
    class Meta:
        verbose_name_plural = "post categories"

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=100, default="")
    img = models.ImageField(default='author_default.jpg', upload_to='profile_pics')
    slug = models.SlugField(unique=True, default="")

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    timestamp = models.DateField(default=timezone.now, auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.user.username} likes \'{self.post.quote}\''


class QuoteCollections(models.Model):
    name = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100, default="")
    img = models.ImageField(default='default.jpg', upload_to='quote_pics', verbose_name="Collection BG Img") 

    draft = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)

    published = models.DateTimeField(default=timezone.now, auto_now=False, auto_now_add=False)
    date_posted = models.DateTimeField(default=timezone.now)

    quote = models.ManyToManyField('Post')

    class Meta:
        verbose_name_plural = "Quote Collections"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(QuoteCollections, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


