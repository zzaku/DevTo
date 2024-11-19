from django.db import models
from accounts.models import User
from posts.models import Post

class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('funny', 'Funny'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    type = models.CharField(max_length=20, choices=REACTION_TYPES)

    def __str__(self):
        return f"{self.type} by {self.user.username} on {self.post.id}"
