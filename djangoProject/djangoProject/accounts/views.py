from django.contrib.auth import get_user_model
from rest_framework import generics as auth_views, status
from rest_framework import views as api_views
from rest_framework import permissions
from rest_framework.authtoken import views as auth_token_views

from djangoProject.accounts.serializers import UserSerializer

UserModel = get_user_model()


# Create your views here.
class UserCreateView(auth_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginUserApiView(auth_token_views.ObtainAuthToken):
    permission_classes = [permissions.AllowAny]


class LogoutUserApiView(api_views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return api_views.Response(status=status.HTTP_200_OK)
