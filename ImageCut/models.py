from django.db import models

# Create your models here.


class TempImage(models.Model) :
    image = models.ImageField(upload_to='tempIamge')

