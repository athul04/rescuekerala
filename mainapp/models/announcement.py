from django.db import models

from mainapp.utils.model_utils import upload_to


class HashTag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Announcements(models.Model):
    ANNOUNCEMENT_PRIORITIES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low')]
    dateadded = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=20,
        choices=ANNOUNCEMENT_PRIORITIES,
        verbose_name='Priority',
        default='L')

    description = models.TextField(blank=True)
    hashtags = models.ManyToManyField(blank=True, to=HashTag, help_text="Add hashtags as comma separated values.")
    image = models.ImageField(blank=True, upload_to=upload_to)
    upload = models.FileField(blank=True, upload_to=upload_to)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Announcement: News'
        verbose_name_plural = 'Announcements: News'

    def __str__(self):
        return self.description[:100]


