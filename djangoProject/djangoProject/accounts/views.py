from rest_framework import generics as api_views, status, permissions
from rest_framework import views as auth_views
from rest_framework.response import Response

from .forms import UserRegisterForm
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .serializers import UserSerializer
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

User = get_user_model()


def verify_email_sent(request):
    return render(request, "user/verifying_email_sent.html")


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        login(request, user)
        user.save()
        messages.success(request, "Your email has been verified.")
        return redirect("verify_email_complete")
    else:
        messages.warning(request, "The link is invalid.")
    return render(request, "user/verify_email_confirm.html")


def verify_email_complete(request):
    return render(request, "user/verify_email_complete.html")


class SignupAPIView(auth_views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            send_verification_email(request, user)
            return Response({"message": "User registered. Please verify your email."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = "Verify Email"
    message = render_to_string("user/verify_email_message.html", {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "request": request,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()
# TODO: Create home page view
