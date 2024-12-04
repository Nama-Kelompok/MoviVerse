# utils/actor.py

from .sparql import wikidata_sparql, local_sparql
from .image import fetch_image

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

def fetch_cast_uri(uri, nama):
    uriid = uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT * WHERE {{
        wd:{uriid} wdt:P31 wd:Q11424 ;
            wdt:P161 ?cast.
        ?cast rdfs:label ?nama
        FILTER(?nama = "{nama}"@en) 
    }} LIMIT 1
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        result = results["results"]["bindings"][0]

        return result["cast"]["value"]

    except Exception as e:
        return {"error": str(e)}

def process_actors(data_movie):
    """
    Process actors from data_movie and update the 'stars' field.

    Args:
        data_movie (dict): The movie data dictionary.

    Returns:
        list of dict: Updated list of actors with 'label', 'uri', and 'image'.
    """
    stars = data_movie.get("stars", "").split(", ")
    movie_wikidata_uri = data_movie.get("wikidataUri", "")

    # Mengambil nama aktor lokal
    local_actor_names = set()
    actors_final = []

    for star_uri in stars:
        if star_uri.strip():
            star_label = fetch_label(star_uri.strip())
            uri_star = fetch_cast_uri(data_movie["wikidataUri"], star_label)
            if isinstance(uri_star, dict) and "error" in uri_star:
                local_actor_names.add(star_label)
                actors_final.append({
                    "label": star_label,
                    "uri": None,
                    "image": None 
                })
            else:
                local_actor_names.add(star_label)
                actors_final.append({
                    "label": star_label,
                    "uri": uri_star,
                    "image": None 
                })
    
    # Mengambil nama aktor dari wikidata dengan limit 20
    if movie_wikidata_uri.startswith("http://www.wikidata.org/entity/"):
        movie_id = movie_wikidata_uri.split('/')[-1]
        sparql_query_wikidata = f"""
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?actor ?actorLabel ?image WHERE {{
            wd:{movie_id} wdt:P161 ?actor .
            OPTIONAL {{ ?actor wdt:P18 ?image. }}
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 20
        """
        wikidata_sparql.setQuery(sparql_query_wikidata)
        try:
            wd_results = wikidata_sparql.query().convert()
            for wd_result in wd_results["results"]["bindings"]:
                actor_label = wd_result["actorLabel"]["value"]
                actor_uri = wd_result["actor"]["value"]
                actor_image = wd_result.get("image", {}).get("value", None)
                if actor_label not in local_actor_names:
                    actors_final.append({
                        "label": actor_label,
                        "uri": actor_uri,
                        "image": actor_image 
                    })
        except Exception as e:
            print(f"Error fetching actors from Wikidata: {e}")

    # Mengambil foto untuk setiap aktor
    for actor in actors_final:
        if actor["image"] is None and actor["uri"]:
            actor_image = fetch_image(actor["uri"])
            actor["image"] = actor_image

    return actors_final