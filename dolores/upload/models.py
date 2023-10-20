from django.db import models

class Partitura(models.Model):
    titolo = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='partiture/')

