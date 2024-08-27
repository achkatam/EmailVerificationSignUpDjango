from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include([
        path("auth/", include("djangoProject.accounts.urls")),

        # YOUR PATTERNS
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ])),
]