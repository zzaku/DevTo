# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post

from .models import User
from .forms import UserUpdateForm
from comments.models import Comment

def home_view(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
        return redirect('home')

    return render(request, 'accounts/home.html', {'posts': posts})

def signup_view(request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            username = request.POST['username']
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/signup.html')

def login_view(request):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = User.objects.get(email=email) 
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password")
                return render(request, "accounts/login.html")

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home") 
            else:
                messages.error(request, "Invalid email or password")
                return render(request, "accounts/login.html")

        return render(request, "accounts/login.html")

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('user_update')

    def get_object(self):
        return self.request.user

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('signup')

    def get_object(self):
        return self.request.user
