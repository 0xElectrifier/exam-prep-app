from django.urls import path
from .views import TextExtraction,ExtractedTextList

urlpatterns = [
    path('extract/', TextExtraction.as_view(), name='extract_text'),
    path('extracted-texts/', ExtractedTextList.as_view(), name='extracted_texts'),
]
