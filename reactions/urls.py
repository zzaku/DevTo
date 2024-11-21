from django.urls import path
from .views import ReactionCreateView, ReactionDeleteView

urlpatterns = [
    path('post/<int:post_id>/reaction/new/', ReactionCreateView.as_view(), name='reaction_create'),
    path('reaction/<int:pk>/delete/', ReactionDeleteView.as_view(), name='reaction_delete'),
]
