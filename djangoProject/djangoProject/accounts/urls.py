from django.urls import path
from djangoProject.accounts.views import UserCreateView, LoginUserApiView

urlpatterns = [
    path("signup/", UserCreateView.as_view(), name="sign_up"),
    path("login/", LoginUserApiView.as_view(), name="login"),
]