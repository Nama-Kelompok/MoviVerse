from django.urls import path
from main.views import movie_page, search_movies, get_movie_data

app_name = 'main'

urlpatterns = [
    path('', search_movies, name='search_movies'),
    path('wiki/<str:id>', movie_page, name='movie_page'),
    path('entity/<str:id>', get_movie_data, name='get_movie_data'),
]
