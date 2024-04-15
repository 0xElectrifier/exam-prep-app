from django.db import models


class BaseModel(models.Model):
    """
    ``BaseModel``: an abstract class with commonly used fields,
        ``updated_at`` and ``created_at``.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True

    def update(self, save=True, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if save:
            self.save()
