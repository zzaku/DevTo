from django.db import models
from accounts.models import CustomUser
from posts.models import Post, Tag

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"


class NewsFeed(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='newsfeed')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NewsFeed for {self.user.username}"
