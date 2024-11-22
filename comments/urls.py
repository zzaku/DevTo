from django.urls import path
from .views import comment_post

urlpatterns = [
    path('', comment_post, name='comment_post'),
]
