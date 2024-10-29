from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse 
from django.urls import reverse
from SPARQLWrapper import SPARQLWrapper

# page detail
def movie_page(request, id):
    context = {"id": id}
    return render(request, "detail.html", context)

# page search
def search_movies(request):
    context = {}
    return render(request, "main.html", context)

# detail of movie
def get_movie_data(request, id):
    # print(request.headers)
    user_agent: str = request.headers["user-agent"]
    if not user_agent.find("Mozilla"):
        # sparql = SPARQLWrapper("https://wikidata/sparql")
        return HttpResponseRedirect(reverse('main:movie_page', kwargs={"id": id}))

    context = {"id": id}
    return JsonResponse(context)
