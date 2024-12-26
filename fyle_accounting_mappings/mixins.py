from django.db import models


class AutoAddCreateUpdateInfoManager(models.Manager):
    def update_or_create(self, defaults=None, **kwargs):
        """
        Overrides the default update_or_create to handle 'user' keyword argument.
        """
        user = kwargs.pop("user", None)
        defaults = defaults or {}

        if user and hasattr(user, "email"):
            defaults["updated_by"] = user.email

        instance, created = super().update_or_create(defaults=defaults, **kwargs)

        if created and user and hasattr(user, "email"):
            instance.created_by = user.email
            instance.save(user=user)

        return instance, created


class AutoAddCreateUpdateInfoMixin(models.Model):
    """
    Mixin to automatically set created_by and updated_by fields.
    Stores only the user's email.
    """

    created_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Email of the user who created this record",
    )
    updated_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Email of the user who last updated this record",
    )

    objects = AutoAddCreateUpdateInfoManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override the save method to set created_by and updated_by fields.
        Expects a 'user' keyword argument containing the user instance.
        """
        user = kwargs.pop('user', None)
        if user and hasattr(user, 'email'):
            if not self.pk:
                self.created_by = user.email
            self.updated_by = user.email
        super().save(*args, **kwargs)
