from django.urls import path
from .views import signup_view, login_view, home_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
