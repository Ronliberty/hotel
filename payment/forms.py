from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    amount_paid = forms.DecimalField(label="Amount Paid", max_digits=10, decimal_places=2, required=True)
    balance = forms.DecimalField(label="Balance", max_digits=10, decimal_places=2, required=False, disabled=True)

    class Meta:
        model = Payment
        fields = ['total_payment', 'payment_type', 'served_by', 'amount_paid']

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)  # Get the order instance
        super().__init__(*args, **kwargs)

        if self.order:
            self.fields['total_payment'].initial = self.order.total_price  # Set the order total
            self.fields['total_payment'].widget.attrs['readonly'] = True  # Make it readonly

    def clean(self):
        cleaned_data = super().clean()
        total_payment = self.order.total_price
        amount_paid = cleaned_data.get('amount_paid')


        # Calculate balance
        cleaned_data['balance'] = total_payment - amount_paid
        return cleaned_data
