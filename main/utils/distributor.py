from .sparql import wikidata_sparql

def fetch_all_distributors(movie_uri):
    print(f"Fetching reviews for movie URI: {movie_uri}")
    uriid = movie_uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?distributor ?label ?logo WHERE {{
        wd:{uriid} wdt:P750 ?distributor .
        ?distributor rdfs:label ?label .
        OPTIONAL {{ ?distributor wdt:P154 ?logo. }} 
        FILTER(LANG(?label) = "en")
    }}
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        distributors = []
        for binding in results["results"]["bindings"]:
            distributor = {
                "label": binding["label"]["value"],
                "uri": binding["distributor"]["value"],
                "logo": binding["logo"]["value"] if "logo" in binding else None
            }
            distributors.append(distributor)
        return distributors
    except Exception as e:
        print(f"Error fetching all distributors: {e}")
        return []
