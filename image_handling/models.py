from django.db import models
from authentication.models import CustomUser

class Image(models.Model):
    image_id = models.CharField(max_length=100, primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_id

