from django.contrib import admin
from bonfire_quotes.admin import admin_site
from django import forms
from .models import Post, Category, Author, Background, PostCategory, PostBackground, Like, QuoteCollections


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = []


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostBackgroundInline(admin.TabularInline):
    model = PostBackground
    extra = 1


class PostAdmin(admin.ModelAdmin):
    form = PostForm

    inlines = [PostCategoryInline, PostBackgroundInline]
    list_display = ('quote', 'author', 'feature_qotd', 'featured_as_qotd', 'featured_date')
    list_filter = ('date_posted',)


class QuoteCollectionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


admin_site.register(Post, PostAdmin)
admin_site.register(Category)
admin_site.register(Background)
admin_site.register(Author)
admin_site.register(Like)
admin_site.register(QuoteCollections, QuoteCollectionsAdmin)
