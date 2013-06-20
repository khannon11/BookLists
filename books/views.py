from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django import forms
from django.contrib.auth import authenticate, login, logout

from books.models import Book, Review, Recommendation

# Create your views here.

def register(request):
  user_form = UserCreationForm(request.POST)
  if user_form.is_valid():
    username = user_form.clean_username()
    password = user_form.clean_password2()
    user_form.save()
    user = authenticate(username=username,
                        password=password)
    login(request, user)
    return redirect("profile")
  return render(request,
                'register.html',
                { 'user_form' : user_form })

@login_required
def profile(request):
  my_reviews = Review.objects.filter(review_author=request.user)
  recommended_for_me = Recommendation.objects.filter(rec_for=request.user)
  my_recommendations = Recommendation.objects.filter(rec_from=request.user)
  return render_to_response('profile.html',
                            {'reviews': my_reviews,
                             'recs_for_me': recommended_for_me,
                             'recs_by_me': my_recommendations},
                            context_instance=RequestContext(request))

def logout_user(request):
  logout(request)
  return profile(request)

class BookForm(ModelForm):
  class Meta:
    model = Book
    fields = ['isbn', 'title', 'author', 'description']

@login_required
def addBook(request):
  if request.method == 'POST':
    form = BookForm(request.POST)
    if form.is_valid():
      form.save()
      return profile(request)
  form = BookForm()
  return render_to_response('addBook.html', {'form': form},
                            context_instance=RequestContext(request))

class NewRecForm(forms.Form):
  rec_for = forms.CharField()
  isbn = forms.CharField()
  text = forms.CharField()

class NewReviewForm(forms.Form):
  isbn = forms.CharField()
  rating = forms.IntegerField()
  text = forms.CharField()

@login_required
def addReview(request):
  if request.method == 'POST':
    form = NewReviewForm(request.POST)
    if form.is_valid():
      isbn = Book.objects.filter(isbn=form.cleaned_data['isbn'])
      if isbn:
        new_review = Review(review_author = request.user,
                             book = isbn[0],
                             rating = form.cleaned_data['rating'],
                             text = form.cleaned_data['text'])
        new_review.save()
        return profile(request)
  form = NewReviewForm()
  return render_to_response('addReview.html', {'form': form},
                            context_instance=RequestContext(request))

def view_review(request, id_num):
  review = Review.objects.filter(id=id_num)[0]
  return render_to_response('review.html', {'review': review},
                            context_instance=RequestContext(request))

def view_rec(request, id_num):
  rec = Recommendation.objects.filter(id=id_num)[0]
  return render_to_response('rec.html', {'rec': rec},
                            context_instance=RequestContext(request))

@login_required
def newRec(request):
  if request.method == 'POST':
    form = NewRecForm(request.POST)
    if form.is_valid():
      rec_for_user = User.objects.filter(username=form.cleaned_data['rec_for'])
      isbn = Book.objects.filter(isbn=form.cleaned_data['isbn'])
      if rec_for_user and isbn:
        rec = Recommendation(rec_from = request.user,
                             rec_for = rec_for_user[0],
                             book = isbn[0],
                             text = form.cleaned_data['text'])
        rec.save()
        return profile(request)
  form = NewRecForm()
  return render_to_response('addRec.html', {'form': form},
                            context_instance=RequestContext(request))
