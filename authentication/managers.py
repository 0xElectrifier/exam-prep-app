from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Manager class for the ``authentication.models.CustomUser`` class.
    """

    def create_user(self, email=None, password=None, save=False, **kwargs):
        email = self.normalize_email(email)
        if not email:
            raise exceptions.ValidationError(
                errors={'email': _("Email not provided.")}
            )
        user, created = self.get_or_create(email=email)
        if created:
            user.set_password(password)
            user.save(using=self._db)
        else:
            if user.is_email_verified:
                raise exceptions.ValidationError(
                    message=_(
                    "Email address has already been taken"
                ))

        return (user, created)
