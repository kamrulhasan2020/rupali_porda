"""
models for database
tables are created according to those classes
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image


class Genre(models.Model):
    genre = models.TextField()
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.genre


class Person(models.Model):
    full_name = models.CharField(max_length=250)
    intro = models.TextField()
    image = models.ImageField(default='default person.jpg', upload_to='peoples')
    date_of_birth = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank = True)

    def __str__(self):
        return self.full_name
    def save(self, *args, **kwargs):
        self.slug = self.slug or (slugify(self.full_name) +  slugify(self.intro))
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 700 or img.width > 700:
            out_size = (700,700)
            img.thumbnail(out_size)
            img.save(self.image.path)



class Movie(models.Model):
    movie_title = models.TextField()
    poster = models.ImageField(default='default poster.jpg', upload_to='posters')
    release_date = models.DateField()
    official_trailer = models.URLField()
    country_of_origin = models.TextField()
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
    duration = models.CharField(max_length=700)
    awards = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    num_of_rating = models.BigIntegerField(default=0)
    total_rating = models.BigIntegerField(default=0)
    num_of_reviews = models.BigIntegerField(default=0)
    average_rating = models.BigIntegerField(default=0)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.movie_title
    def save(self, *args, **kwargs):
        self.slug = self.slug or (slugify(self.movie_title) + slugify(self.genre) + slugify(str(self.release_date)))
        super().save(*args, **kwargs)
        img = Image.open(self.poster.path)
        if img.height > 700 or img.width > 700:
            out_size = (700,700)
            img.thumbnail(out_size)
            img.save(self.poster.path)


class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character = models.CharField(max_length=250, blank=True, null=True)
    star = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.person.full_name


class Director(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.person.full_name

class Producer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.person.full_name


class Crew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    role = models.CharField(max_length=250)

    def __str__(self):
        return self.name



class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.BigIntegerField()




class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review= models.TextField()
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = self.slug or (slugify(self.user) + slugify(self.movie.movie_title) +slugify(str(self.date)))
        super().save(*args,**kwargs)
