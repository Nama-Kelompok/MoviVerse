from .sparql import wikidata_sparql, local_sparql
from .image import fetch_image  
from .actor import fetch_label 

def fetch_director_uri(uri, nama):
    uriid = uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?director WHERE {{
        wd:{uriid} wdt:P57 ?director .
        ?director rdfs:label "{nama}"@en
    }} LIMIT 1
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["director"]["value"]
        else:
            print(f"No director URI found for {nama}")
            return {"error": f"No director URI found for {nama}"}
    except Exception as e:
        print(f"Error fetching director URI for {nama}: {e}")
        return {"error": str(e)}

def process_director(data_movie):
    director_uri = data_movie.get("director", "")
    if director_uri.startswith("http://"):
        # Mengambil nama director di wikidata
        director_label = fetch_label(director_uri)
        uri_director = fetch_director_uri(data_movie["wikidataUri"], director_label)
        if isinstance(uri_director, dict) and "error" in uri_director:
            # Jika terjadi error saat mengambil URI director
            director_image = None
            director_uri_final = None
        else:
            director_image = fetch_image(uri_director) if uri_director else None
            director_uri_final = uri_director

        data_movie["director"] = {
            "label": director_label,
            "image": director_image,
            "uri": director_uri_final,
        }
    else:
        # Mengambil nama director jika tidak ada di lokal
        director_label = "Tidak terdapat data director"
        director_uri_final = None
        director_image = None
        if data_movie.get("wikidataUri", "").startswith("http://www.wikidata.org/entity/"):
            movie_id = data_movie["wikidataUri"].split('/')[-1]
            sparql_query_director_wikidata = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?director ?directorLabel ?image WHERE {{
                wd:{movie_id} wdt:P57 ?director .
                OPTIONAL {{ ?director wdt:P18 ?image. }}
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            LIMIT 1
            """
            wikidata_sparql.setQuery(sparql_query_director_wikidata)
            try:
                director_wd_results = wikidata_sparql.query().convert()
                if director_wd_results["results"]["bindings"]:
                    director_label = director_wd_results["results"]["bindings"][0]["directorLabel"]["value"]
                    director_uri = director_wd_results["results"]["bindings"][0]["director"]["value"]
                    director_image = director_wd_results["results"]["bindings"][0].get("image", {}).get("value", None)
                    if director_image is None and director_uri:
                        director_image = fetch_image(director_uri)
                    data_movie["director"] = {
                        "label": director_label,
                        "image": director_image,
                        "uri": director_uri,
                    }
                else:
                    data_movie["director"] = {"label": director_label, "image": director_image, "uri": director_uri_final}
            except Exception as e:
                print(f"Error fetching director from Wikidata: {e}")
                data_movie["director"] = {"label": director_label, "image": director_image, "uri": director_uri_final}
        else:
            data_movie["director"] = {"label": director_label, "image": director_image, "uri": director_uri_final}

    return data_movie