from django.db import models

# Create your models here.

class ImageData(models.Model):
    image = models.ImageField(upload_to='DATA/')

    def __str__(self):
        return self.image.url
