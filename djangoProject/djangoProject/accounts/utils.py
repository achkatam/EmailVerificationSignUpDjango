
from django.contrib.auth import tokens as auth_tokens
from django.core import mail
from django.template.loader import render_to_string
from django.utils import encoding
from django.conf import settings
from django.utils import http

def send_verification_email(self, user):
    token = auth_tokens.default_token_generator.make_token(user)
    uid = http.urlsafe_base64_encode(encoding.force_bytes(user.pk))
    verification_link = f"{settings.FRONTEND_URL}/verify_email/?uid={uid}&token={token}"
    message = render_to_string("user/verify_email.html", {"verification_link": verification_link})
    mail.send_mail(
        "Verify your email address",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
