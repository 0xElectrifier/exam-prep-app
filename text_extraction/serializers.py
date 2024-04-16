from rest_framework import serializers
from .models import ExtractedText

class ExtractedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedText
        fields = ['text_id', 'image', 'user_id', 'extracted_text', 'extracted_at']
        read_only_fields = ['extracted_at']

class PostTextExtractionRequestSerializer(serializers.Serializer):
    image_id = serializers.CharField()