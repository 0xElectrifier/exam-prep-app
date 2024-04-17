from django.db import models

from core.models import BaseModel
from core.utils import generate_id

class Summary(BaseModel):

    summary_id = models.CharField(max_length=40, default=generate_id)
    extracted_text = models.ForeignKey(
        "text_extraction.ExtractedText",
        on_delete=models.SET_NULL, null=True
    )
    summary_content = models.CharField(max_length=4096, null=True)

    def __str__(self):
        return self.summary_content[:16]
