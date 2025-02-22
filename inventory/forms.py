from django import forms
from .models import Product, TaxCategory, SubCategory, SalesInvoice

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sub_category', 'name', 'description', 'sales_price', 'discount', 'qty', 'cost_price', 'unit',
                  'tax_category', 'volume', 'weight', 'currency']
        widgets = {
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sales_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_category': forms.Select(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),

        }
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})  # Adds 'form-control' to all fields

class TaxCategoryForm(forms.ModelForm):
    class Meta:
        model = TaxCategory
        fields = ['tax_category', 'tax_desc', 'tax_percentage']

        widgets = {
            'tax_category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tax category name'}),
            'tax_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter tax percentage'}),
        }



class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['main_category', 'name', 'description']
        widgets = {
              # Normal select field
            'name': forms.TextInput(attrs={'class': '', 'placeholder': 'Enter SubCategory Name'}),
            'description': forms.Textarea(attrs={'class': '', 'rows': 3, 'placeholder': 'Enter Description'}),
        }


class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = [
            'invoice_number', 'bought_at', 'product', 'qty_sold',
            'sales_price', 'discount', 'tax_category', 'tax_amount',
            'total_amount', 'currency', 'issued_by'
        ]
        widgets = {
            'bought_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }