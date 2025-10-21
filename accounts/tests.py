from django.test import TestCase
from django.urls import resolve, reverse

from .models import ShaUser
from accounts.forms import LoginUserForm, RegisterUserForm, ChangeProfileForm
from .views import RegisterUserView, profile, ChangeProfileView, ShaPassChangeView, ShaPassResetView, user_activate, ShaLogin


class UserActivationTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register_activate', args=['sign'])
        self.response = self.client.get(self.url)

    def test_user_activation_url_resolves_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, user_activate)

    def test_user_activation_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)


class PasswordResetPageTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:password_reset')
        self.response = self.client.get(self.url)

    def test_password_reset_url_resolves_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, ShaPassResetView)

    def test_password_reset_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)


class PasswordChangePageTests(TestCase):
    def setUp(self):
        self.user = ShaUser.objects.create_user(username='testuser', password='Password123!')
        self.url = reverse('accounts:password_change')
        self.client.login(username='testuser', password='Password123!')
        self.response = self.client.get(self.url)

    def test_password_change_url_resolves_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, ShaPassChangeView)

    def test_password_change_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_password_change_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/password_change.html')

    def test_user_can_change_password(self):
        response = self.client.post(self.url, {
            'old_password': 'Password123!',
            'new_password1': 'NewPassword456!',
            'new_password2': 'NewPassword456!',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword456!'))


class ChangeProfilePageTests(TestCase):
    def setUp(self):
        self.user = ShaUser.objects.create_user(username='testuser', password='Password123!')
        self.url = reverse('accounts:profile_change')
        self.client.login(username='testuser', password='Password123!')
        self.response = self.client.get(self.url)

    def test_profile_change_url_resolves_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, ChangeProfileView)

    def test_profile_change_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_profile_change_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/change_profile.html')

    def test_user_can_change_profile(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'newemail@example.com',
            'location-TOTAL_FORMS': '1',
            'location-INITIAL_FORMS': '0',
            'location-MIN_NUM_FORMS': '0',
            'location-MAX_NUM_FORMS': '1000',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'newemail@example.com')


class ProfilePageTests(TestCase):
    def setUp(self):
        self.user = ShaUser.objects.create_user(username='testuser', password='Password123!')
        self.url = reverse('accounts:profile')
        self.client.login(username='testuser', password='Password123!')
        self.response = self.client.get(self.url)

    def test_profile_url_resolves_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, profile)

    def test_profile_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_profile_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/profile.html')

    def test_profile_page_displays_user_info(self):
        self.assertContains(self.response, self.user.username)


class RegistrationPageTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register_user')
        self.response = self.client.get(self.url)

    def test_registration_url_resolves_to_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, RegisterUserView)

    def test_registration_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_registration_template_used(self):
        self.assertTemplateUsed(self.response, 'accounts/register_user.html')

    def test_registration_form_present(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegisterUserForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_user_can_register(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ShaUser.objects.filter(username='newuser').exists())


class LoginPageTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.response = self.client.get(self.url)

    def test_login_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, ShaLogin)

    def test_login_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, LoginUserForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        self.assertIn('username', form.as_p())
        self.assertIn('password', form.as_p())

    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertContains(self.response, 'Login')

    def test_user_can_login(self):
        ShaUser.objects.create_user(username='testuser', password='Password123!')
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile'))



