from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from posts.models import Post
from django.contrib.auth.decorators import login_required

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'comments/comment_form.html'
    

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})
    
@login_required
def comment_post(request, post_id):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post.objects.get(id=post_id)
        Comment.objects.create(user=request.user, post=post, content=content)
        return redirect('home')

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'comments/comment_form.html'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
