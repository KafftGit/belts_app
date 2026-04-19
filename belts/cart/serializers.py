from rest_framework import serializers


class CartItemCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemUpdateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CartItemChangeSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    action = serializers.ChoiceField(choices=["increase", "decrease"])


class CartItemDeleteSerializer(serializers.Serializer):
    product = serializers.IntegerField()


class CartCompleteSerializer(serializers.Serializer):
    recipient_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=30)
    city = serializers.CharField(max_length=120)
    street = serializers.CharField(max_length=255)
    house = serializers.CharField(max_length=30)
    apartment = serializers.CharField(max_length=30, required=False, allow_blank=True)
    entrance = serializers.CharField(max_length=30, required=False, allow_blank=True)
    floor = serializers.CharField(max_length=30, required=False, allow_blank=True)
    intercom = serializers.CharField(max_length=30, required=False, allow_blank=True)
    postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    extra_notes = serializers.CharField(required=False, allow_blank=True)