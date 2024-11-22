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

from .models import Post, Comment, Reaction
from .forms import PostForm


class HomePageView(TemplateView):
    template_name = "posts/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(status="Published")
        return context


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"  # Customize this as needed
    success_url = reverse_lazy("posts:home")  # Replace with your post list URL name

    def form_valid(self, form):
        # Automatically associate the logged-in user with the post
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
            # Remove the reaction if it already exists
            existing_reaction.delete()
        else:
            # Add a new reaction and ensure no duplicate reactions
            Reaction.objects.update_or_create(
                user=request.user, post=post, reaction_type=reaction_type
            )

        return redirect("posts:post_detail", pk=pk)
