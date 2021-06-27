from django.contrib import admin
from .models import Genre, Person, Movie, Cast, Crew, Producer, Director, Rating, Review
"""
registering models to the admin site 
"""

admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Movie)
admin.site.register(Cast)
admin.site.register(Crew)
admin.site.register(Producer)
admin.site.register(Director)
admin.site.register(Rating)
admin.site.register(Review)
