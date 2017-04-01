from django.db import models
from django.dispatch import receiver
import os


class UploadedFile(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " at " + self.file.url


# Delete the file on disk when its model is deleted from the db
@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_on_disk(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
