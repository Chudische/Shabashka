from django.test import TestCase
from django.urls import reverse, resolve

from .models import SuperCategory, SubCategory, Offer
from accounts.models import ShaUser
from .views import index, services, by_category, detail, add_new_offer


class OfferCreatePageTests(TestCase):
    def setUp(self):
        self.user = ShaUser.objects.create_user(username='testuser', password='Password123!')
        self.super_category = SuperCategory.objects.create(name='Test Super Category')
        self.sub_category = SubCategory.objects.create(name='Test Sub Category', super_category=self.super_category)
        self.url = reverse('main:add_new_offer')
        self.client.login(username='testuser', password='Password123!')

    def test_offer_create_url_resolves_add_new_offer_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, add_new_offer)

    def test_offer_create_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_offer_create_page_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main/add_new_offer.html')

    def test_user_can_create_offer(self):
        response = self.client.post(self.url, {
            'title': 'New Offer',
            'content': 'New Content',
            'price': 100,
            'category': self.sub_category.pk,
            'author': self.user.pk,
            'additionalimage_set-TOTAL_FORMS': '1',
            'additionalimage_set-INITIAL_FORMS': '0',
            'additionalimage_set-MIN_NUM_FORMS': '0',
            'additionalimage_set-MAX_NUM_FORMS': '1000',
            'location-TOTAL_FORMS': '1',
            'location-INITIAL_FORMS': '0',
            'location-MIN_NUM_FORMS': '0',
            'location-MAX_NUM_FORMS': '1000',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Offer.objects.filter(title='New Offer').exists())


class OfferDetailPageTests(TestCase):
    def setUp(self):
        self.user = ShaUser.objects.create_user(username='testuser', password='Password123!')
        self.super_category = SuperCategory.objects.create(name='Test Super Category')
        self.sub_category = SubCategory.objects.create(name='Test Sub Category', super_category=self.super_category)
        self.offer = Offer.objects.create(title='Test Offer', content='Test Content', author=self.user, category=self.sub_category)
        self.url = reverse('main:detail', args=[self.sub_category.pk, self.offer.pk])
        self.response = self.client.get(self.url)

    def test_offer_detail_url_resolves_detail_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, detail)

    def test_offer_detail_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_offer_detail_page_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'main/detail.html')


class CategoryPageTests(TestCase):
    def setUp(self):
        self.super_category = SuperCategory.objects.create(name='Test Super Category')
        self.sub_category = SubCategory.objects.create(name='Test Sub Category', super_category=self.super_category)
        self.url = reverse('main:by_category', args=[self.sub_category.pk])
        self.response = self.client.get(self.url)

    def test_category_url_resolves_by_category_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, by_category)

    def test_category_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_category_page_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'main/by_category.html')


class ServicesPageTests(TestCase):
    def setUp(self):
        self.url = reverse('main:services')
        self.response = self.client.get(self.url)

    def test_services_url_resolves_services_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, services)

    def test_services_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_services_page_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'main/services.html')


class HomePageTests(TestCase):
    def setUp(self):
        self.url = reverse('main:index')
        self.response = self.client.get(self.url)

    def test_homepage_url_resolves_index_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, index)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'main/index.html')
