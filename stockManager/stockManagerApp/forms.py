from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
