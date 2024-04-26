from django.db import models
from books.models import Book

# Create your models here.
class Sale(models.Model):
  # defining attributes of the class
  # connected to Book model, will delete entries across models for a deleted book
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  price = models.FloatField()
  date_created = models.DateTimeField(auto_now_add=True)

  # string representation for a sale
  def __str__(self):
    return f"ID: {self.id}, book: {self.book.name}, quantity: {self.quantity}"