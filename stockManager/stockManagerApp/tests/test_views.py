from django.test import TestCase, SimpleTestCase
from stockManagerApp.models import Item
from django.urls import reverse
from django.forms.models import model_to_dict
from decimal import Decimal


class HomeViewTest(SimpleTestCase):

    def test_home_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class ItemsListViewTest(TestCase):
    def setUp(self):
        Item.objects.create(name="Limpol", quantity=200,
                            price=2.0, vendor_name="Bombril")
        Item.objects.create(name="Amido de Milho", quantity=200,
                            price=7.0, vendor_name="Maizena")

    def test_items_list_view_get(self):
        response = self.client.get(reverse("items_list"))
        self.assertEqual(response.status_code, 200)
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


class CreateItemViewTest(TestCase):

    def test_create_item_view_get(self):
        response = self.client.get(reverse("create_item"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_item.html")
        self.assertContains(response, "<form", count=1)
        self.assertContains(response, 'name="name"', count=1)
        self.assertContains(response, 'name="quantity"', count=1)
        self.assertContains(response, 'name="price"', count=1)
        self.assertContains(response, 'name="vendor_name"', count=1)

    def test_create_item_view_valid_post(self):
        test_item = {
            "name": "Pendrive 32gb",
            "quantity": 20,
            "price": 20,
            "vendor_name": "SanDisk"
        }
        response = self.client.post(reverse("create_item"), test_item)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("items_list"))

        self.assertEqual(Item.objects.count(), 1)
        item_dict = model_to_dict(
            Item.objects.first(), fields=['name', 'quantity', 'price', 'vendor_name'])
        self.assertEqual(item_dict, test_item)

    def test_create_item_view_invalid_post(self):
        test_item = {
            "name": "",
            "quantity": 20,
            "price": 20,
            "vendor_name": "SanDisk"
        }
        response = self.client.post(reverse("create_item"), test_item)
        self.assertEqual(response.status_code, 200)


class EditItemViewTest(TestCase):
    def setUp(self):
        Item.objects.create(name="Pendrive 32gb", quantity=200,
                            price=20, vendor_name="SanDisk")

    def test_create_item_view_get(self):
        item = Item.objects.get(name="Pendrive 32gb")
        response = self.client.get(
            reverse("edit_item", kwargs={"id": item.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_item.html")
        self.assertContains(response, "<form", count=1)
        self.assertContains(response, 'name="name"', count=1)
        self.assertContains(response, 'name="quantity"', count=1)
        self.assertContains(response, 'name="price"', count=1)
        self.assertContains(response, 'name="vendor_name"', count=1)

    def test_edit_item_view_post_valid(self):
        test_item_modified = {
            "name": "Pendrive 16gb",
            "quantity": 20,
            "price": Decimal("19.99"),
            "vendor_name": "SanDisk"
        }
        item = Item.objects.get(name="Pendrive 32gb")
        response = self.client.post(
            reverse("edit_item", kwargs={"id": item.id}), test_item_modified)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("items_list"))

        self.assertEqual(Item.objects.count(), 1)

        item_dict = model_to_dict(
            Item.objects.first(), fields=['name', 'quantity', 'price', 'vendor_name'])
        self.assertEqual(item_dict, test_item_modified)

    def test_edit_item_view_invalid_post(self):
        test_item = {
            "name": "",
            "quantity": 20,
            "price": 20,
            "vendor_name": "SanDisk"
        }
        item = Item.objects.get(name="Pendrive 32gb")
        response = self.client.post(
            reverse("edit_item", kwargs={"id": item.id}), test_item)
        self.assertEqual(response.status_code, 200)


class DeleteItemViewTest(TestCase):
    def setUp(self):
        Item.objects.create(name="Pendrive 32gb", quantity=200,
                            price=20, vendor_name="SanDisk")

    def test_delete_item_view_valid_post(self):
        item = Item.objects.get(name="Pendrive 32gb")
        response = self.client.post(
            reverse("delete_item", kwargs={"id": item.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("items_list"))
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_item_view_invalid_post(self):
        response = self.client.post(reverse("delete_item", kwargs={"id": 0}))
        self.assertEqual(response.status_code, 404)
