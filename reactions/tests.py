from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post
from reactions.models import Like

# Plus à jour
class LikePostViewTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.other_user = get_user_model().objects.create_user(username='otheruser', email='other@example.com', password='otherpassword')
        
        self.post = Post.objects.create(user=self.other_user, content="Test Post Content")
        
        self.url = reverse('like_post', kwargs={'post_id': self.post.id})
    
    def test_like_post_view_redirect_for_anonymous_user(self):
        """ Vérifie que l'utilisateur non authentifié est redirigé vers la page de login. """
        response = self.client.post(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_like_post_view_for_authenticated_user(self):
        """ Vérifie qu'un utilisateur authentifié peut "liker" un post. """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        
        self.assertRedirects(response, reverse('home'))
        
        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.first()
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
    
    def test_like_post_view_only_once(self):
        """ Vérifie qu'un utilisateur ne peut pas "liker" le même post plusieurs fois. """
        self.client.login(username='testuser', password='testpassword')
        
        self.client.post(self.url)
        self.assertEqual(Like.objects.count(), 1)
        
        self.client.post(self.url)
        self.assertEqual(Like.objects.count(), 1)
    
    def test_like_post_view_for_other_user(self):
        """ Vérifie qu'un utilisateur ne peut pas "liker" le post d'un autre utilisateur. """
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(self.url)
        
        self.assertRedirects(response, reverse('home'))
        
        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.first()
        self.assertEqual(like.user, self.other_user)
        self.assertEqual(like.post, self.post)
