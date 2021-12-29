from django.db import models


# Create your models here.
class Uploads(models.Model):
    name = models.CharField(max_length=100)
    matric_no = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    info = models.CharField(max_length=100)
