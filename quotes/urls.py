from django.urls import path
from .views import  PostDetailView, PostDeleteView
from . import views

urlpatterns = [
    path('', views.home, name="quotes-home"),
    path('quote-of-the-day', views.quotes_day, name="quotes-day"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/', views.update_post, name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/<int:pk>/like/<int:like_val>/', views.like_post, name='post-like'),
    path('post/new', views.create_post, name="post-create"),
    path('post/preview', views.preview_post, name="post-preview"),
    path('about/', views.about, name="quotes-about"),
    path('community/', views.community, name="quotes-community"),
]
