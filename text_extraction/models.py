from django.db import models
from image_handling.models import Image
from core.utils import generate_id
from authentication.models import CustomUser

class ExtractedText(models.Model):
    text_id = models.CharField(default=generate_id(),max_length=255, primary_key=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    extracted_text = models.TextField()
    extracted_at = models.DateTimeField(auto_now_add=True)