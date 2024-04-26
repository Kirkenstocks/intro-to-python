from django.test import TestCase
from .models import Book

# Create your tests here.
class BookModelTest(TestCase):
  # set up non-modified object used by all test methods
  def setUpTestData():
    Book.objects.create(
      name='Pride and Prejudice', author_name='Jane Austen', genre='classic',
      book_type='hardcover', price='23.71'
    )

  # unit test to check if book name is rendered correctly
  def test_book_name(self):
    # get the book object to test
    book = Book.objects.get(id=1)

    # get the metadata for 'name' field and use it to query its data
    field_label = book._meta.get_field('name').verbose_name

    # compare value to expected result
    self.assertEqual(field_label, 'name')

  # check if author name is under the 120 ccharacter max length
  def test_author_name_max_length(self):
    # same process as test_book_name()
    book = Book.objects.get(id=1)
    max_length = book._meta.get_field('author_name').max_length
    self.assertEqual(max_length, 120)