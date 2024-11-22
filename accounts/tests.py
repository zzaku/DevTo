from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment

# Plus à jour
class HomeViewTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.post = Post.objects.create(user=self.user, content="Test Post Content")
        self.url = reverse('home')
        
    def test_home_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_with_comment(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'post_id': self.post.id,
            'content': 'Test comment',
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, self.url)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.user, self.user)

class SignUpViewTests(TestCase):
    
    def setUp(self):
        self.url = reverse('signup')
    
    def test_signup_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_signup_view_successful_post(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_signup_view_unsuccessful_post(self):
        data = {
            'username': '',
            'email': 'invalidemail',
            'password': '123',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

class LoginViewTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.url = reverse('login')
    
    def test_login_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_successful_post(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_unsuccessful_post_invalid_credentials(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertFormError(response, 'form', None, 'Invalid email or password')
