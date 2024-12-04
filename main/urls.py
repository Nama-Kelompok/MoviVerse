from django.urls import path
from main.views import movie_page, search_movies, get_movie_data, landing_page, main_page, fetch_cast_uri, get_movie_details

app_name = 'main'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('wiki/<str:id>', movie_page, name='movie_page'),
    path('entity/<str:id>', get_movie_data, name='get_movie_data'),
    path("movie/<path:uri>/", get_movie_details, name="movie_detail"),
    path("search", search_movies, name="search_movie"),
    path("main_search", main_page, name="main_page"),
    path("cast/<path:uri>/<str:nama>/", fetch_cast_uri, name="fetch_cast")
]
