from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from SPARQLWrapper import SPARQLWrapper, JSON

host = "http://localhost:7200"
local_sparql = SPARQLWrapper(f"{host}/repositories/Nama-Kelompok")
local_sparql.setReturnFormat(JSON)


# page detail
def movie_page(request, id):
    context = {"id": id}
    return render(request, "detail.html", context)

# page detail
def landing_page(request):
    return render(request, "landing.html")

# page search
def search_movies(request):
    context = {}
    print("awtawd")
    return render(request, "main.html", context)


# detail of movie
def get_movie_data(request, id):
    user_agent = request.headers.get("user-agent", "")
    if "Mozilla" not in user_agent:
        return HttpResponseRedirect(reverse("main:movie_page", kwargs={"id": id}))

    context = {"id": id}
    return JsonResponse(context)


def get_movie_details(request, uri=None):
    print("Mengambil detail film untuk URI:", uri)

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

        FILTER (?movies = <{uri}>)
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

            # Ambil label untuk stars
            stars = data_movie.get("stars", "").split(", ")
            data_movie["stars"] = []
            for star_uri in stars:
                if star_uri.strip():
                    star_label = fetch_label(star_uri.strip())
                    data_movie["stars"].append(star_label)

            # Ambil label untuk director
            director_uri = data_movie.get("director", "")
            if director_uri.startswith("http://"):
                director_label = fetch_label(director_uri)
                data_movie["director"] = director_label
            else:
                data_movie["director"] = "Tidak terdapat data director"

            return render(request, "detail_movie.html", {"movie": data_movie})
        else:
            return JsonResponse({"error": "Film tidak ditemukan"}, status=404)

    except Exception as e:
        # Jika terjadi error, kembalikan error sebagai JSON
        return JsonResponse({"error": str(e)}, status=500)
    

def fetch_label(uri):

    sparql_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label WHERE {{
        <{uri}> rdfs:label ?label .
    }}
    LIMIT 1
    """
    local_sparql.setQuery(sparql_query)

    try:
        # Eksekusi query
        results = local_sparql.query().convert()
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["label"]["value"]
        else:
            return "Label tidak ditemukan"
    except Exception as e:
        print(f"Error fetching label for {uri}: {e}")
        return "Error fetching label"

