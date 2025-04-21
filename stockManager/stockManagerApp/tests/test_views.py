from django.test import TestCase, SimpleTestCase
from stockManagerApp.models import Item
from django.urls import reverse


class HomeViewTest(SimpleTestCase):

    def test_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ItemsListViewTest(TestCase):
    def setUp(self):
        Item.objects.create(name="Limpol", quantity=200,
                            price=2.0, vendor_name="Bombril")
        Item.objects.create(name="Amido de Milho", quantity=200,
                            price=7.0, vendor_name="Maizena")

    def test_status_code(self):
        response = self.client.get(reverse("items_list"))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse("items_list"))
        self.assertTemplateUsed(response, "items.html")

    def test_items_context(self):
        response = self.client.get(reverse("items_list"))
        self.assertEqual(len(response.context["items"]), 2)
        self.assertContains(response, "Limpol")
        self.assertContains(response, "Amido de Milho")
        self.assertNotContains(response, "Nenhum item cadastrado")

    def test_no_items_context(self):
        Item.objects.all().delete()
        response = self.client.get(reverse("items_list"))
        self.assertEqual(len(response.context["items"]), 0)
        self.assertContains(response, "Nenhum item cadastrado")
