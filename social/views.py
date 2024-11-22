from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Follow, NewsFeed

class NewsFeedListView(LoginRequiredMixin, ListView):
    model = NewsFeed
    template_name = 'social/newsfeed_list.html'
    context_object_name = 'newsfeed'

    def get_queryset(self):
        return NewsFeed.objects.filter(user=self.request.user).order_by('-created_at')

class FollowCreateView(LoginRequiredMixin, CreateView):
    model = Follow

    def form_valid(self, form):
        followed_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        form.instance.follower = self.request.user
        form.instance.followed = followed_user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.kwargs['user_id']})

class FollowDeleteView(LoginRequiredMixin, DeleteView):
    model = Follow

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def get_success_url(self):
        return reverse_lazy('newsfeed')
