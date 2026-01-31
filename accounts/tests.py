from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .views import HomePageView, SignUpView, AddressCreateView, AddressUpdateView, AddressDeleteView


# Create your tests here.

class HomePageViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', 'testuser@email.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')
        url = reverse('accounts:home')
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Your orders')

    # check right view function used
    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)



class SignUpPageTests(TestCase):
    username = 'testuser'
    email = 'testuser@email.com'

    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_tempalte(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.__name__, SignUpView.as_view().__name__)


class AddressCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', 'testuser@email.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')
        url = reverse('accounts:address_new')
        self.response = self.client.get(url)
    
    def test_address_create_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)    
    
    def test_address_create_template(self):
        self.assertTemplateUsed(self.response, 'address_new.html')
    
    def test_address_create_view(self):
        view = resolve('/accounts/address/new/')
        self.assertEqual(view.func.__name__, AddressCreateView.as_view().__name__)


class AddressUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', 'testuser@email.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.address = self.user.addresses.create(
            address1='123 Main Street',
            city='Anytown',
            state='ST',
            postal_code='12345',
            country='USA',
            phone='123-456-7890'
        )
        url = reverse('accounts:address_edit', kwargs={'pk': self.address.pk})
        self.response = self.client.get(url)
    
    def test_address_update_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)    
    
    def test_address_update_template(self):
        self.assertTemplateUsed(self.response, 'address_edit.html')
    
    def test_address_update_view(self):
        view = resolve(f'/accounts/address/{self.address.pk}/edit/')
        self.assertEqual(view.func.__name__, AddressUpdateView.as_view().__name__)

    def test_address_update_forbidden_for_other_users(self):
        other_user = get_user_model().objects.create_user('otheruser', 'otheruser@email.com', 'otherpass123')
        self.client.login(username='otheruser', password='otherpass123')
        url = reverse('accounts:address_edit', kwargs={'pk': self.address.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

class AddressDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', 'testuser@email.com', 'testpass123')   
        self.client.login(username='testuser', password='testpass123')
        self.address = self.user.addresses.create(
            address1='123 Main Street',
            city='Anytown',
            state='ST',
            postal_code='12345',
            country='USA',
            phone='123-456-7890'
        )
        url = reverse('accounts:address_delete', kwargs={'pk': self.address.pk})
        self.response = self.client.get(url)    
    
    def test_address_delete_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)    
    
    def test_address_delete_template(self):
        self.assertTemplateUsed(self.response, 'address_delete.html')
    
    def test_address_delete_view(self):
        view = resolve(f'/accounts/address/{self.address.pk}/delete/')
        self.assertEqual(view.func.__name__, AddressDeleteView.as_view().__name__)
    
    def test_address_delete_forbidden_for_other_users(self):
        other_user = get_user_model().objects.create_user('otheruser', 'otheruser@email.com', 'otherpass123')
        self.client.login(username='otheruser', password='otherpass123')
        url = reverse('accounts:address_delete', kwargs={'pk': self.address.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403) 
