"""
Test File model

Django model for a test file.

=== Fields ===

title --------(char) The title of the file being uploaded.
file --------- (file) The file being uploaded.
uploaded_at -- (dateTime) The time that the file was uploaded.
test --------- (Test) The test associated with the file.


=== Methods ===

__str__ -------------- Returns the string representation of the existing file model.
auto_delete_on_disk -- Deletes the file on the user's disk when the model is deleted from the SQLite database. 

"""

import os

from django.db import models
from django.dispatch import receiver

from .Test import Test


class TestFile(models.Model):
    title = models.CharField(max_length=255, default="An uploaded file")
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test, related_name='Test', verbose_name='Test result', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " at " + self.file.url


# Delete the file on disk when its model is deleted from the db
@receiver(models.signals.post_delete, sender=TestFile)
def auto_delete_on_disk(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
