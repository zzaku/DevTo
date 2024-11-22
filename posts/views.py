from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    View,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post, Comment, Reaction, Tag
from .forms import PostForm


class HomePageView(TemplateView):
    template_name = "posts/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(status="Published")
        context["tags"] = Tag.objects.all()
        return context
    
class PostsByTagView(ListView):
    model = Post
    template_name = "posts/home.html" 
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name")
        return Post.objects.filter(tags__name=tag_name, status="Published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_tag"] = self.kwargs.get("tag_name")
        return context


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("posts:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "post_image", "tags", "status"]
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("posts:home") 

    def form_valid(self, form):
        form.instance.user = (
            self.request.user
        )
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("posts:home") 

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user


class CreateCommentView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, "posts/create_comment.html", {"post": post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
        return redirect("posts:post_detail", pk=pk)


class AddReactionView(View):
    def post(self, request, pk, reaction_type):
        post = get_object_or_404(Post, pk=pk)
        existing_reaction = Reaction.objects.filter(
            user=request.user, post=post, reaction_type=reaction_type
        )

        if existing_reaction.exists():
            existing_reaction.delete()
        else:
            Reaction.objects.update_or_create(
                user=request.user, post=post, reaction_type=reaction_type
            )

        return redirect("posts:post_detail", pk=pk)
