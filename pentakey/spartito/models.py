from django.db import models

class Spartito(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    spartito_image = models.ImageField(upload_to='spartiti/')
    musicxml_file = models.FileField(null=True, blank=True, upload_to='musicxml/')

