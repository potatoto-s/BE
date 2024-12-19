from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views as token_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # API URLs
    path(
        "api/",
        include(
            [
                path("", include("posts.urls")),
                path("", include("comments.urls")),
            ]
        ),
    ),
    # API 문서
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/token/", token_views.obtain_auth_token),
]
