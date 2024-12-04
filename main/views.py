from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .utils.distributor import fetch_all_distributors
from .utils.director import process_director 
from .utils.actor import process_actors
from .utils.review import fetch_review_scores
from .utils.time import format_running_time

from .utils.sparql import local_sparql 

def movie_page(request, id):
    context = {"id": id}
    return render(request, "detail.html", context)

def landing_page(request):
    return render(request, "landing.html")

def main_page(request):
    search = request.GET.get("search", "")
    context = {"search": search}
    return render(request, "main.html", context)

def search_movies(request):
    PAGE_SIZE = 20
    movie = request.GET.get("movie", "")
    page = int(request.GET.get("page", 1))

    sparql_query = f"""
    PREFIX : <http://nama-kelompok.org/data/> 
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX v: <http://nama-kelompok.org/vocab#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT * WHERE {{
        ?movieId rdf:type :Movie .
        ?movieId rdfs:label ?movieName .
        OPTIONAL {{?movieId v:posterLink ?posterLink .}}
        FILTER(REGEX(?movieName, ".*{movie}.*", "i"))
    }} ORDER BY ?movieName
    OFFSET {(page - 1) * PAGE_SIZE}
    LIMIT {PAGE_SIZE + 1}
    """
    local_sparql.setQuery(sparql_query)
    query_results = local_sparql.query().convert()["results"]["bindings"]

    hasNextPage = False
    if len(query_results) > PAGE_SIZE:
        hasNextPage = True
        query_results = query_results[:PAGE_SIZE]

    data = {}
    data["hasNextPage"] = hasNextPage
    data["currentPage"] = page

    movies = []
    for movie in query_results:
        tempData = {}
        tempData["movieId"] = movie['movieId']["value"]
        tempData["movieName"] = movie["movieName"]["value"]
        if "posterLink" in movie:
            tempData["posterLink"] = movie["posterLink"]["value"]
        else:
            tempData["posterLink"] = ""
        movies.append(tempData)

    data["movies"] = movies
    return JsonResponse(data)

# Mengambil data dari movie
def get_movie_data(request, id):
    user_agent = request.headers.get("user-agent", "")
    if "Mozilla" not in user_agent:
        return HttpResponseRedirect(reverse("main:movie_page", kwargs={"id": id}))

    context = {"id": id}
    return JsonResponse(context)

# Mengambil detail dari movie
def get_movie_details(request, uri=None):
    if not uri.startswith("http://"):
        uri = f"http://nama-kelompok.org/data/{uri}"

    # Query SPARQL
    sparql_query = f"""
    PREFIX : <http://nama-kelompok.org/data/> 
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX v: <http://nama-kelompok.org/vocab#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?movies ?title ?director 
           (GROUP_CONCAT(DISTINCT ?genre; separator=", ") AS ?genres) 
           ?rating ?metaScore ?information ?photoUrl ?releaseYear ?runningTime 
           (GROUP_CONCAT(DISTINCT ?star; separator=", ") AS ?stars) 
           ?votes ?wikidataUri ?distributor
    WHERE {{
        ?movies rdf:type :Movie .
        ?movies rdfs:label ?title .
        
        OPTIONAL {{ ?movies v:director ?director. }}
        OPTIONAL {{ ?movies v:distributor ?distributor. }}
        OPTIONAL {{ ?movies v:genre ?genre. }}
        OPTIONAL {{ ?movies v:imdbRating ?rating. }}
        OPTIONAL {{ ?movies v:metaScore ?metaScore. }}
        OPTIONAL {{ ?movies v:movieInfo ?information. }}
        OPTIONAL {{ ?movies v:posterLink ?photoUrl. }}
        OPTIONAL {{ ?movies v:releaseYear ?releaseYear. }}
        OPTIONAL {{ ?movies v:runningTime ?runningTime. }}
        OPTIONAL {{ ?movies v:star ?star. }}
        OPTIONAL {{ ?movies v:votes ?votes. }}
        OPTIONAL {{ ?movies v:wikidataUri ?wikidataUri. }}
        VALUES ?movies {{ <{uri}> }} 
    }}
    GROUP BY ?movies ?title ?director ?rating ?metaScore ?information 
             ?photoUrl ?releaseYear ?runningTime ?votes ?wikidataUri ?distributor
    LIMIT 1
    """
    local_sparql.setQuery(sparql_query)

    try:
        results = local_sparql.query().convert()

        attributes = [
            "director", "genres", "rating", "metaScore", "information",
            "photoUrl", "releaseYear", "runningTime", "stars", "votes", "wikidataUri", "distributor"
        ]

        if results["results"]["bindings"]:
            result = results["results"]["bindings"][0]
            data_movie = {
                "movies": result["movies"]["value"],
                "title": result["title"]["value"],
            }

            for attr in attributes:
                data_movie[attr] = result[attr]["value"] if attr in result else f"Tidak terdapat data {attr}"

            # Mengambil nama aktor
            actors_final = process_actors(data_movie)
            data_movie["stars"] = actors_final

            # Mengambil nama distributor
            distributors = fetch_all_distributors(data_movie["wikidataUri"])
            data_movie["distributors"] = distributors

            # Mengambil nama director menggunakan fungsi process_director
            data_movie = process_director(data_movie)

            # Mengambil running time film
            running_time = data_movie.get("runningTime", "")
            data_movie["runningTime"] = format_running_time(running_time)

            # Mengambil review scores
            reviews = fetch_review_scores(data_movie["wikidataUri"])

            # Tambahkan placeholder untuk properti yang kosong
            for review in reviews:
                review["reviewer_uri"] = review.get("reviewer_uri", "#") 
                review["reviewer_label"] = review.get("reviewer_label", "Unknown Reviewer")

            data_movie["reviews"] = reviews


            return render(request, "detail_movie.html", {"movie": data_movie})

        else:
            return JsonResponse({"error": "Film tidak ditemukan"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)