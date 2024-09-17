from django.urls import path
from .views import (signup_view,
                    # verify_email,
                   verify_email_sent, verify_email_confirm,
                   verify_email_complete)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    # path("verify_email/", verify_email, name="verify_email"),
    path("verify_email_sent/", verify_email_sent, name="verify_email_sent"),
    path("verify_email_confirm/<uidb64>/<token>/", verify_email_confirm, name="verify_email_confirm"),
    path("verify_email/complete/", verify_email_complete, name="verify_email_complete"),
]
