from rest_framework import serializers
from .models import FlashcardCategory
from .models import Flashcard

class ImageSerializerField(serializers.RelatedField):
    def to_representation(self, value):
        return value.image_url
    
class CategorySerializerField(serializers.RelatedField):
    def to_representation(self, value):
        return value.category_name

class FlashcardRequestSerializer(serializers.Serializer):
    number_of_cards = serializers.IntegerField(max_value=15)
    text = serializers.CharField()
    category = serializers.IntegerField()

class FlashcardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashcardCategory
        fields = ['id', 'category_name', 'created_at']

class FlashcardSerializer(serializers.ModelSerializer):
    image = ImageSerializerField(read_only=True)
    category = CategorySerializerField(read_only=True)
    class Meta:
        model = Flashcard
        fields = ['id', 'category', 'question', 'answer', 'image', 'created_at', 'updated_at']