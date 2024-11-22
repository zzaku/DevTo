from django.urls import path
from .views import DashboardView, SignupView, UserLoginView, user_logout, UserUpdateView, UserDeleteView

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
]
