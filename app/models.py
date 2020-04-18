import os

from django.db import models

class ImageModel(models.Model):
    file = models.ImageField(verbose_name='Image', upload_to='img/', blank=True, null=True)

    def filename(self):
        return os.path.basename(self.file.name)