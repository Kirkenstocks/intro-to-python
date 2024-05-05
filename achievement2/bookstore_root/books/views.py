from django.shortcuts import render
from django.views.generic import ListView, DetailView
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book

# Create your views here.
class BookListView(LoginRequiredMixin, ListView):
  model = Book
  template_name = 'books/main.html'

class BookDetailView(LoginRequiredMixin, DetailView):
  model = Book
  template_name = 'books/details.html'
