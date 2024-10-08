from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary_storage.storage import MediaCloudinaryStorage
from django_resized import ResizedImageField
from django.utils.text import slugify


class Profile(models.Model):
    """Profile model"""

    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    image = ResizedImageField(
        size=[300, 300],
        quality=75,
        upload_to="profiles/",
        force_format="WEBP",
        blank=False,
        storage=MediaCloudinaryStorage(),
    )
    bio = RichTextField(max_length=2500, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.user.id}")
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
