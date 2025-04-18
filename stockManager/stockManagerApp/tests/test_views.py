from django.test import TestCase, SimpleTestCase
from stockManagerApp.models import Item
from django.urls import reverse


class homeTest(SimpleTestCase):

    def test_statusCode(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_correctTemplate(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class itemsTest(TestCase):
    def setUp(self):
        Item.objects.create(name="Limpol", quantity=200,
                            price=2, vendorName="Bombril")
        Item.objects.create(name="Amido de Milho", quantity=200,
                            price=7, vendorName="Maizena")

    def test_statusCode(self):
        response = self.client.get(reverse("itens"))
        self.assertEqual(response.status_code, 200)

    def test_correctTemplate(self):
        response = self.client.get(reverse("itens"))
        self.assertTemplateUsed(response, "items.html")

    def test_itemsContext(self):
        response = self.client.get(reverse("itens"))
        self.assertEqual(len(response.context["items"]), 2)
        self.assertContains(response, "Limpol")
        self.assertContains(response, "Amido de Milho")
        self.assertNotContains(response, "Nenhum item cadastrado")

    def test_noItemsContext(self):
        Item.objects.all().delete()
        response = self.client.get(reverse("itens"))
        self.assertEqual(len(response.context["items"]), 0)
        self.assertContains(response, "Nenhum item cadastrado")
