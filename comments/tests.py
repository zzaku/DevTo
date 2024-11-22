from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment

class CommentPostViewTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        self.post = Post.objects.create(user=self.user, content="Test Post Content")

        self.url = reverse('comment_post', kwargs={'post_id': self.post.id})
    
    def test_comment_post_view_redirect_for_anonymous_user(self):
        """ Vérifie que l'utilisateur non authentifié est redirigé vers la page de login. """
        response = self.client.post(self.url, {'content': 'Test comment'})
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_comment_post_view_for_authenticated_user(self):
        """ Vérifie qu'un utilisateur authentifié peut ajouter un commentaire. """
        self.client.login(username='testuser', password='testpassword')
        data = {'content': 'Test comment'}
        response = self.client.post(self.url, data)
        
        self.assertRedirects(response, reverse('home'))
        
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
    
    def test_comment_post_view_without_content(self):
        """ Vérifie qu'un commentaire vide n'est pas ajouté. """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'content': ''})
        
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
