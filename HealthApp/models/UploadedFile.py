"""
Uploaded File model

Django model for a uploaded file.

=== Fields ===

title ------- (char) The title of the file being uploaded.
file -------- (file) The file being uploaded.
uploaded_at - (dateTime) The time that the file was uploaded.


=== Methods ===

__str__ ------------- Returns the string representation of the existing file model.
auto_delete_on_disk - Deletes the file on the user's disk when the model is deleted from the SQLite database. 

"""

from django.db import models
from django.dispatch import receiver
import os


class UploadedFile(models.Model):
    title = models.CharField(max_length=255, default="An uploaded file")
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " at " + self.file.url


# Delete the file on disk when its model is deleted from the db
@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_on_disk(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
