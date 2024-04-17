from rest_framework import serializers
from .models import FlashcardCategory
from .models import Flashcard

class ImageSerializerField(serializers.RelatedField):
    def to_representation(self, value):
        return value.image_url

class FlashcardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashcardCategory
        fields = ['id', 'category_name', 'created_at']

class FlashcardSerializer(serializers.ModelSerializer):
    image = ImageSerializerField(read_only=True)
    class Meta:
        model = Flashcard
        fields = ['id', 'category', 'question', 'answer', 'image', 'created_at', 'updated_at']