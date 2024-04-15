from django.urls import path
from .views import ImageUploadAPIView, ImageDeleteAPIView

urlpatterns = [
    path('upload/', ImageUploadAPIView.as_view(), name='image_upload'),
    path('<image_id>/', ImageDeleteAPIView.as_view(), name='image_delete'),
]
