from django.urls import path
from .views import (
    create_post
)
from .views import PhotoCreateView

urlpatterns = [
    path('', create_post, name='create_post'),
]
