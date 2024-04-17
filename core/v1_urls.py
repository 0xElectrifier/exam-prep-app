from django.urls import include, path
from dj_rest_auth.registration.views import RegisterView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('auth/', include('dj_rest_auth.urls'), name="rest_auth"),
    path('auth/signup/', include('dj_rest_auth.registration.urls')),
    path("",include("user_management.urls"), name="user_management"),
    path("images/", include("image_handling.urls"), name="image_handling"),
    path("text/", include("text_extraction.urls"), name="text_extraction"),
    path("summarize/", include("text_summarization.urls"), name="text_summarization"),
]
