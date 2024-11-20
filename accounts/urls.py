from django.urls import path
from .views import SignupView, UserLoginView, UserLogoutView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
]
