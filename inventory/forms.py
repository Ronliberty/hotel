from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sub_category', 'name', 'description', 'sales_price', 'discount', 'qty', 'cost_price', 'unit',
                  'tax_category', 'volume', 'weight', 'currency']
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})  # Adds 'form-control' to all fields
