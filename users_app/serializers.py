from rest_framework import serializers
from .models import User


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'address', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        user.email = validated_data.get('email', '')
        user.address = validated_data.get('address', '')
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'email', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']