from django.test import TestCase
from django.urls import reverse
from stockManagerApp.models import Item


class ItemFormTest(TestCase):
    def test_createItemWhenIsValid(self):
        testItem = {
            "name": "Pendrive 32gb",
            "quantity": 20,
            "price": 20,
            "vendorName": "SanDisk"
        }
        response = self.client.post(reverse("createItem"), data=testItem)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(name="Pendrive 32gb").exists())

    def test_dontCreateItemWhenIsInvalid(self):
        testItem = {
            "name": "",
            "quantity": -4,
            "price": -20,
            "vendorName": ""
        }
        response = self.client.post(reverse("createItem"), data=testItem)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)

        form = response.context["form"]
        self.assertFormError(form, "name", "This field is required.")
        self.assertFormError(form, "quantity", "Quantity cannot be negative")
        self.assertFormError(form, "price", "Price cannot be negative")
        self.assertFormError(form, "vendorName", "This field is required.")

        self.assertFalse(Item.objects.exists())
