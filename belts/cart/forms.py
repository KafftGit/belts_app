from django import forms


class CartCreateForm(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1)
    unit_price = forms.IntegerField()

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError("Количество должно быть не меньше 1")
        return quantity


class CartItemUpdateForm(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError("Количество должно быть не меньше 1")
        return quantity


class CartItemDeleteForm(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput())


class CartCompleteForm(forms.Form):
    recipient_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=30)
    city = forms.CharField(max_length=120)
    street = forms.CharField(max_length=255)
    house = forms.CharField(max_length=30)
    apartment = forms.CharField(max_length=30, required=False)
    entrance = forms.CharField(max_length=30, required=False)
    floor = forms.CharField(max_length=30, required=False)
    intercom = forms.CharField(max_length=30, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    extra_notes = forms.CharField(required=False)

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        allowed = set("0123456789+()- ")
        if not all(ch in allowed for ch in phone):
            raise forms.ValidationError("Телефон содержит недопустимые символы")
        if len([ch for ch in phone if ch.isdigit()]) < 10:
            raise forms.ValidationError("Укажите корректный номер телефона")
        return phone

    def clean_city(self):
        city = self.cleaned_data["city"].strip()
        if not city:
            raise forms.ValidationError("Поле «Город» обязательно")
        return city

    def clean_street(self):
        street = self.cleaned_data["street"].strip()
        if not street:
            raise forms.ValidationError("Поле «Улица» обязательно")
        return street

    def clean_house(self):
        house = self.cleaned_data["house"].strip()
        if not house:
            raise forms.ValidationError("Поле «Дом» обязательно")
        return house