from django import forms
from .models import Crop,Order,Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'image', 'price_per_kg', 'quantity_available','category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter crop name'}),
            'price_per_kg': forms.NumberInput(attrs={'min': '0'}),
            'quantity_available': forms.NumberInput(attrs={'min': '0'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity_ordered', 'address', 'delivery_address']


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
