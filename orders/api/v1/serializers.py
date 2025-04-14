from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=400,)
    full_name = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=11)
    postal_code = serializers.CharField(max_length=256,)

    
