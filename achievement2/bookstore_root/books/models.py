from django.db import models
from django.shortcuts import reverse

# genre choices are displayed as a dropdown menu
genre_choices = (
  ('classic', 'Classic'),
  ('romantic', 'Romantic'),
  ('comic', 'Comic'),
  ('fantasy', 'Fantasy'),
  ('horror', 'Horror'),
  ('educational', 'Educational')
)

# book type choices displayed as a dropdown menu
book_type_choices = (
  ('hardcover', 'Hard cover'),
  ('ebook', 'E-Book'),
  ('audiobook', 'Audiobook')
)

# Create your models here.
class Book(models.Model):
  # defining attributes of the class
  name = models.CharField(max_length=120)
  author_name = models.CharField(max_length=120)
  price = models.FloatField(help_text= 'in US dollars $')
  genre = models.CharField(max_length=12, choices=genre_choices, default='classic')
  book_type = models.CharField(max_length=12, choices=book_type_choices, default='hardcover')
  pic = models.ImageField(upload_to='books', default='no-image.svg')

  def get_absolute_url(self):
    return reverse ('books:details', kwargs={'pk': self.pk})

  # string representation of the book entry
  def __str__(self):
    return str(self.name)