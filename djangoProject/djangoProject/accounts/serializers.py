from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import tokens as auth_tokens
from django.core import mail
from django.template.loader import render_to_string
from django.utils import encoding
from django.utils import http
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "password")

    # This func should be refactored to send verification email after user creation
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.is_active = True
        user.save()

        self.send_verification_email(user)

        return user

    def send_verification_email(self, user):
        token = auth_tokens.default_token_generator.make_token(user)
        uid = http.urlsafe_base64_encode(encoding.force_bytes(user.pk))
        verification_link = f"{settings.FRONTEND_URL}/verify-email/?uid={uid}&token={token}"
        message = render_to_string('email_verification.html', {'verification_link': verification_link})
        mail.send_mail(
            'Verify your email address',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    def to_representation(self, *args, **kwargs):
        representation = super().to_representation(*args, **kwargs)
        representation.pop("password", None)

        return representation
