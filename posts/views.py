from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Photo, Tag
from .forms import PostForm, PhotoForm
from django.contrib.auth.decorators import login_required

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        Post.objects.create(user=request.user, content=content)
        return redirect('home')
    return render(request, 'posts/create_post.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'posts/photo_form.html'
    form_class = PhotoForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
