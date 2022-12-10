# from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Company(models.Model):
    location = models.PointField()
