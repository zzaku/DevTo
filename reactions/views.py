from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Reaction
from posts.models import Post

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
