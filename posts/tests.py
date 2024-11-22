from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post

# Plus à jour
class CreatePostViewTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        self.url = reverse('create_post')
    
    def test_create_post_view_redirect_for_anonymous_user(self):
        """ Vérifie que l'utilisateur non authentifié est redirigé vers la page de login. """
        response = self.client.post(self.url, {'content': 'Test Post Content'})
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_create_post_view_for_authenticated_user(self):
        """ Vérifie qu'un utilisateur authentifié peut créer un post. """
        self.client.login(username='testuser', password='testpassword')
        data = {'content': 'Test Post Content'}
        response = self.client.post(self.url, data)
        
        self.assertRedirects(response, reverse('home'))
        
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.content, 'Test Post Content')
        self.assertEqual(post.user, self.user)
    
    def test_create_post_view_without_content(self):
        """ Vérifie qu'un post vide ne peut pas être créé. """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'content': ''})
        
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
