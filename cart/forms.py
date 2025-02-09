from .models import MenuCategory, MenuItem
from django import forms





class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(
                attrs={'class': 'custom-input', 'rows': 3, 'placeholder': 'Enter category description'}),
        }








class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'description', 'price', 'is_available', 'currency', 'volume', 'weight', 'unit']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter menu item name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter item description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter volume'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter weight'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit'}),
        }
