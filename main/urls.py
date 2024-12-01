from django.urls import path
from main.views import movie_page, search_movies, get_movie_data, main_page
from . import views

app_name = 'main'

urlpatterns = [
    path('', main_page, name='search_movies'),
    path('wiki/<str:id>', movie_page, name='movie_page'),
    path('entity/<str:id>', get_movie_data, name='get_movie_data'),
    path("movie/<path:uri>/", views.get_movie_details, name="movie_detail"),
    path("search", search_movies, name="search_movie")
]
