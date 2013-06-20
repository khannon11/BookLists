from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
  isbn = models.CharField(max_length=20)
  title = models.CharField(max_length=100)
  author = models.CharField(max_length=50)
  description = models.CharField(max_length=1000)

class Review(models.Model):
  review_author = models.ForeignKey(User)
  book = models.ForeignKey(Book)
  rating = models.IntegerField(default=4)
  text = models.CharField(max_length=1000)

class Recommendation(models.Model):
  rec_from = models.ForeignKey(User, related_name='+')
  rec_for = models.ForeignKey(User, related_name='+')
  book = models.ForeignKey(Book)
  text = models.CharField(max_length=1000)
