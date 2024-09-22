from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout as auth_logout
from rentals.models import Book, Rental
from django.contrib import messages
import requests
from unittest.mock import patch


class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        # Create a test book
        self.book = Book.objects.create(title='Test Book', author='Test Author', number_of_pages=123)

    def test_home_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/home.html')

    @patch('requests.get')
    def test_search_books_view(self, mock_get):
        self.client.login(username='testuser', password='testpassword')
        mock_response = {
            'docs': [
                {
                    'key': '/works/OL123W',
                    'title': 'Test Book',
                    'author_name': ['Test Author'],
                    'number_of_pages_median': 123
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        
        response = self.client.get(reverse('search_books') + '?title=Test Book')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/search_books.html')
        self.assertContains(response, 'Test Book')


    def test_extend_rental_view(self):
        self.client.login(username='testuser', password='testpassword')
        rental = Rental.objects.create(user=self.user, book=self.book)
        response = self.client.get(reverse('extend_rental', args=[rental.id]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        rental.refresh_from_db()  # Check if rental is extended



    def test_admin_dashboard_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/admin_dashboard.html')

    def test_admin_dashboard_view_access_denied(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'rentals/error.html')

    def test_rental_dashboard_view(self):
        self.client.login(username='testuser', password='testpassword')
        Rental.objects.create(user=self.user, book=self.book)
        response = self.client.get(reverse('rental_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/rental_dashboard.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/auth/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_failure(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/auth/login.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/auth/register.html')



    def test_dashboard_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/auth/dashboard.html')
