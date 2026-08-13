from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CategoryAccessTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fruits")
        self.product = Product.objects.create(
            category=self.category,
            name="Apple",
            price="1.50",
            stock=10,
        )

    def test_unauthenticated_user_cannot_access_category(self):
        url = reverse("catalog:product_list_by_category", args=[self.category.slug])
        response = self.client.get(url)

        self.assertRedirects(response, f"{reverse('register')}?next={url}")

    def test_authenticated_user_can_access_category(self):
        User.objects.create_user(username="the_user", password="the_password")
        self.client.login(username="the_user", password="the_password")

        url = reverse("catalog:product_list_by_category", args=[self.category.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple")
