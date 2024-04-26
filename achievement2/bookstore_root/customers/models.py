from django.db import models

# Create your models here.
class Customer(models.Model):
  # defining attributes
  name = models.CharField(max_length=120)
  notes = models.TextField(default='no notes')

  # string representation for class
  def __str__(self):
    return str(self.name)

