from django import forms

from utils.validators import validate_user_items


class OrderCreateForm(forms.Form):
    items = forms.JSONField()
    address = forms.CharField()
    extra_notes = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_items(self):
        items = self.cleaned_data.get("items")
        if not isinstance(items, list) or not items:
            raise forms.ValidationError("Отсутствуют товары")

        validated_data = validate_user_items(items=items)

        self.cleaned_data.update(validated_data)
        return items
