from pyexpat import model
from django.db import models

class contactform(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

