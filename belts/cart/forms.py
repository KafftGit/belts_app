from django import forms


class CartCreateForm(forms.Form):
    quantity = forms.IntegerField(initial=1)
    unit_price = forms.IntegerField()
    product = forms.IntegerField(widget=forms.HiddenInput())


class CartItemDeleteForm(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput())


class CartCompleteForm(forms.Form):
    address = forms.CharField()
    extra_notes = forms.CharField(required=False)
