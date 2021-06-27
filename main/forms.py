"""
django generates htmls from accroding to this classes
"""
from django import forms
from .models import Rating, Review
RATING_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
]

class RatingForm(forms.ModelForm):
    rating=forms.IntegerField(label="Your Rating:", widget=forms.Select(choices=RATING_CHOICES))
    class Meta:
        model = Rating
        fields = [
            'rating'
        ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'review'
        ]

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=400)
    class Meta:
        fields = [
        'keyword'
        ]
