from django.test import TestCase
from django.urls import reverse
from stockManagerApp.models import Item


class ItemFormTest(TestCase):
    def test_create_item_when_is_valid(self):
        test_item = {
            "name": "Pendrive 32gb",
            "quantity": 20,
            "price": 20,
            "vendor_name": "SanDisk"
        }
        response = self.client.post(reverse("create_item"), data=test_item)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(name="Pendrive 32gb").exists())

    def test_dont_create_item_when_is_invalid(self):
        test_item = {
            "name": "",
            "quantity": -4,
            "price": -20,
            "vendor_name": ""
        }
        response = self.client.post(reverse("create_item"), data=test_item)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)

        form = response.context["form"]
        self.assertFormError(form, "name", "This field is required.")
        self.assertFormError(form, "quantity", "Quantity cannot be negative.")
        self.assertFormError(form, "price", "Price cannot be negative.")
        self.assertFormError(form, "vendor_name", "This field is required.")

        self.assertFalse(Item.objects.exists())
