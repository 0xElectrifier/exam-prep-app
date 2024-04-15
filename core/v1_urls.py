from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('auth/', include('dj_rest_auth.urls'), name="rest_auth"),
    path("",include("user_management.urls"), name="user_management")
]
