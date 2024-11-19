from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_photo = models.URLField(null=True, blank=True)
    technologies = models.ManyToManyField('Technology', related_name='users', blank=True)
    languages = models.ManyToManyField('Language', related_name='users', blank=True)

    def stats(self):
        """Calcul des statistiques de l'utilisateur"""
        return {
            'posts_count': self.posts.count(),
            'comments_count': self.comments.count(),
            'reactions_count': self.reactions.count(),
        }


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
