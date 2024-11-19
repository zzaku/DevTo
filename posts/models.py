from django.db import models
from accounts.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_photos')
    url = models.URLField()

    def __str__(self):
        return f"Photo {self.id} for {self.post or self.user.username}"
