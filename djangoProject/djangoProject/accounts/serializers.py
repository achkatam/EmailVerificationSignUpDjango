from django.contrib.auth import get_user_model
from rest_framework import serializers
from utils import send_verification_email

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "password")

    # This func should be refactored to send verification email after user creation
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        send_verification_email(user)

        return user

    def to_representation(self, *args, **kwargs):
        representation = super().to_representation(*args, **kwargs)
        representation.pop("password", None)

        return representation
