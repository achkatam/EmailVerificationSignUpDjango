from django.contrib.auth import get_user_model
from rest_framework import serializers

from djangoProject.accounts.utils import send_verification_email

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ("email", "password", "confirm_password")

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = UserModel.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        send_verification_email(user)

        return user

    def to_representation(self, *args, **kwargs):
        representation = super().to_representation(*args, **kwargs)
        representation.pop("password", None)

        return representation
