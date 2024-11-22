from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from reactions.forms import ReactionForm
from .models import Like, Reaction
from posts.models import Post
from django.contrib.auth.decorators import login_required

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.get_or_create(user=request.user, post=post)
    return redirect('home')

class ReactionCreateView(LoginRequiredMixin, CreateView):
    model = Reaction
    fields = ['type']  
    template_name = 'reactions/reaction_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

class ReactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Reaction
    template_name = 'reactions/reaction_confirm_delete.html'

    def get_queryset(self):
        return Reaction.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})
