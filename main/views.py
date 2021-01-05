from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Movie, Genre, Rating, Review, Person
from .forms import RatingForm, ReviewForm, SearchForm


class Home(ListView):
    """
    Displays the home page of the site.
    Shows 4 most recently released movies
    """
    template_name = 'main/home.html'
    context_object_name = 'MovieList'
    form = SearchForm


    def get_queryset(self):
        """
        returns the queryset to perform
        """
        return Movie.objects.order_by('-release_date')[:4] #filters 4 most recently released movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context



class ShowMovieDetails(DetailView):
    """
    Shows details of a movie object.
    """
    model = Movie
    template_name = 'main/movie.html'
    context_object_name = 'Movie'
    slug_field = 'slug'


    def get_context_data(self, **kwargs):
        """
        returns conetext data which will be used in template files.
        """
        context = super().get_context_data(**kwargs)
        movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
        context['Director'] = movie.director_set.all()
        context['Producer'] = movie.producer_set.all()
        context['Cast'] = movie.cast_set.all()
        return context


class GenreMovieList(ListView):
    """
    returns movies derived from a specific genre
    """
    template_name = 'main/genre_movie_list.html'
    context_object_name = 'MovieList'


    def get_queryset(self):
        """
        returns queryset to perform
        """
        self.genre = get_object_or_404(Genre, genre=self.kwargs['genre'])
        return Movie.objects.filter(genre=self.genre)



    def get_context_data(self, **kwargs):
        """
        returns context data which will be used in templates
        """
        context = super().get_context_data(**kwargs)
        context['Genre'] = self.genre
        return context


class Rate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    """
    This view rates a specific movie
    """
    form_class = RatingForm #form used to rate movies, imported from froms.py
    template_name = 'main/rate.html'
    success_message = "Your rating was added"


    def form_valid(self, form):
        """
        performs some operations if the submitted is valid
        """
        form.instance.user = self.request.user #populate user field with the user who made this request
        form.instance.movie = self.movie #populates movie filed
        #following lines updates the number of rating, total rating and avg.rating of the movie
        rating = form.cleaned_data['rating']
        self.movie.total_rating += rating
        self.movie.num_of_rating += 1
        self.movie.average_rating = self.movie.total_rating / self.movie.num_of_rating
        form.save() #saves the rating object to the database
        self.movie.save()
        return super().form_valid(form)


    def get_success_url(self):
        """
        returns success url
        """
        return reverse('main:home')


    def test_func(self):
        """
        makes sure that the user has permission to rate the movie
        One user can rate a movie for one time only
        """
        self.movie = get_object_or_404(Movie, slug=self.kwargs['slug']) #gets the movie
        try:
            #checks whether user has rated this movie or not
            rating = Rating.objects.get(user=self.request.user, movie=self.movie)
        except Rating.DoesNotExist:
            return True # if user didn't rate this movie earlier he/she has the permission to rate this movie
        return False # returns false user already rated this movie


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    This view deletes review
    """
    model = Review
    success_message = 'Your review is deleted'
    template_name = 'main/check_delete.html'
    slug_field = 'slug'


    def get_success_url(self):
        """
        returns the success url, url to redirect after deleting a review
        """
        movie = self.review.movie
        movie.num_of_reviews -= 1
        movie.save()
        return reverse('main:home')


    def test_func(self):
        """
        checks whether the user has the permission to delete the review or not
        only the person who wrote the review can delete
        """
        self.review = get_object_or_404(self.model, slug=self.kwargs['slug'])
        if self.review.user == self.request.user:
            return True
        return False


class UpdateReview(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    this view updates/edits a review
    """
    model = Review
    fields = ['review']
    template_name = 'main/review_update.html'


    def get_success_url(self):
        """
        returns the success url, url to redirect after updating a review
        """
        return reverse('main:home')


    def test_func(self):
        """
        checks whether user has the permission to update the review or not.
        only the user who wrote that review can update it
        """
        self.review = get_object_or_404(self.model, slug=self.kwargs['slug'])
        if self.review.user == self.request.user:
            return True
        return False


class ShowReviews(ListView):
    """
    this views shows all the reviews of a movie
    """
    template_name = 'main/review_list.html'
    context_object_name = 'ReviewList'


    def get_queryset(self):
        """
        returns queryset
        """
        self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
        return self.movie.review_set.all()


    def get_context_data(self, **kwargs):
        """
        return context data, which is used in templates
        """
        context = super().get_context_data(**kwargs)
        context['movie'] = self.movie
        return context






class WriteReview(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, FormView):
    """
    creates a review object of a movie
    """
    template_name = 'main/review.html'
    form_class = ReviewForm
    success_message = 'Your review was added'


    def form_valid(self, form):
        """
        performs following actions if the submitted form is valid
        """
        form.instance.user = self.request.user
        form.instance.movie = self.movie
        self.movie.num_of_reviews += 1
        form.save()
        self.movie.save()
        return super().form_valid(form)


    def get_success_url(self):
        """
        return success url
        """
        return reverse('main:home')


    def test_func(self):
        """
        checks whether user has the permission to write a review or not
        One user can write one review only for a specific movie
        """
        self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
        try:
            review = Review.objects.get(user=self.request.user, movie=self.movie)
        except Review.DoesNotExist:
            return True
        return False


class Search(View):
    """
    Serch movies and actors/producers/deirectos/cast&crew
    Primarily It works in a simple way.
    It just matches keyword against movie title and persons name
    and return the result
    """
    form = SearchForm
    template_name = 'main/search_form.html'


    def get(self, request, *args, **kwargs):
        """
        Handles get requests and returns the form
        """
        form = self.form()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        """
        Handles Post request.
        gets keyword from the form
        and returns matching results
        """
        form = self.form(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            MovieList = Movie.objects.filter(movie_title=keyword)
            PersonList = Person.objects.filter(full_name=keyword)
            context = {
                'MovieList':MovieList,
                'PersonList':PersonList
                }
            return render(request, 'main/search_result.html', context)

        return render(request, self.template_name, {'form': form})


class PersonDetails(DetailView):
    """
    Shows the details of Person Object
    """
    model = Person
    template_name = 'main/person.html'
    context_object_name = 'Person'
    slug_field = 'slug'
