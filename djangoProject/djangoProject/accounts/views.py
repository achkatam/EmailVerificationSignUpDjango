from django.contrib.auth import get_user_model
from rest_framework import generics as auth_views, status
from rest_framework import views as api_views
from rest_framework import permissions
from rest_framework.authtoken import views as auth_token_views
from django.utils import http
from django.utils import encoding
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken import models
from rest_framework.response import Response

from djangoProject.accounts.serializers import UserSerializer

UserModel = get_user_model()


class UserCreateView(auth_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class VerifyEmailApiView(api_views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        uid = encoding.force_str(http.urlsafe_base64_decode(request.GET.get('uid')))
        token = request.GET.get('token')
        try:
            user = UserModel.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.is_verified = True  # Mark the email as verified
                user.save()
                return api_views.Response({'status': 'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return api_views.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            return api_views.Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserApiView(auth_token_views.ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Use DRF's built-in authentication to authenticate the user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Check if the user has verified their email
        if not user.is_verified:
            return Response({"detail": "Email not verified."}, status=status.HTTP_403_FORBIDDEN)

        # If email is verified, generate and return the token
        token, created = models.Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LogoutUserApiView(api_views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return api_views.Response(status=status.HTTP_200_OK)
