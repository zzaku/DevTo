from django.urls import reverse
from django.db import models
from accounts.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ("Published", "Published"),
    ("Private", "Private"),
    ("Draft", "Draft"),
)


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=700, db_index=True)
    content = models.TextField()
    post_image = models.ImageField(upload_to="images/", default="images/post1.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Draft")

    def __str__(self):
        return f"Post {self.id} by {self.user}"

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.pk})

    def total_reactions(self):
        return self.posts_reactions.count() or 0
    
    def total_comments(self):
        self.comment_set.all().count()

    def reaction_summary(self):
        return self.posts_reactions.values("reaction_type").annotate(
            count=models.Count("reaction_type")
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.user} | {self.content}"


class Reaction(models.Model):
    REACTION_TYPES = [
        ("like", "❤️"),
        ("laugh", "😄"),
        ("celebrate", "🎉"),
        ("insightful", "💡"),
        ("curious", "🤔"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="users_reactions"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts_reactions")
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)

    class Meta:
        unique_together = (
            "user",
            "post",
            "reaction_type",
        )  # Ensure a user can react only once with the same type.

    def __str__(self):
        return f"{self.user} reacted {self.reaction_type} to {self.post}"
