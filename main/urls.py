"""
maps urls to the views

"""
from django.urls import path
from .import views

app_name = 'main' #name spacing urls
#defines valid url patterns
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('show/<slug:slug>/', views.ShowMovieDetails.as_view(), name='show_movie_details'),
    path('list/<str:genre>/', views.GenreMovieList.as_view(), name='genre_movie_list'),
    path('rate/<slug:slug>/', views.Rate.as_view(), name='rate'),
    path('show-reviews/<slug:slug>/', views.ShowReviews.as_view(), name='show_reviews'),
    path('review/<slug:slug>/', views.WriteReview.as_view(), name='review'),
    path('update-review/<slug:slug>/', views.UpdateReview.as_view(), name='update_review'),
    path('delete-review/<slug:slug>/', views.DeleteReview.as_view(), name='delete_review'),
    path('person/<slug:slug>/', views.PersonDetails.as_view(), name='person_view'),
    path('search', views.Search.as_view(), name='search'),
]
