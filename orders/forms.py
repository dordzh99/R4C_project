from django import forms

from .models import Customer,Order


class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), to_field_name='email')

    class Meta:
        model = Order
        fields = ("robot_serial", "customer",)
