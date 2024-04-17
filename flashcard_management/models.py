from django.db import models
from authentication.models import CustomUser
from image_handling.models import Image

class FlashcardCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

class Flashcard(models.Model):
    category = models.ForeignKey(FlashcardCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50] + "..."