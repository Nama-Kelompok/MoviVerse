from .sparql import wikidata_sparql

def fetch_country_of_origin(movie_uri):
    print(f"Fetching country of origin for movie URI: {movie_uri}")
    uriid = movie_uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?country ?label ?image WHERE {{
        wd:{uriid} wdt:P495 ?country .
        ?country rdfs:label ?label .
        OPTIONAL {{ ?country wdt:P18 ?image. }}
        FILTER(LANG(?label) = "en")
    }}
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        countries = []
        for binding in results["results"]["bindings"]:
            country = {
                "label": binding["label"]["value"],
                "uri": binding["country"]["value"],
                "image": binding["image"]["value"] if "image" in binding else None
            }
            countries.append(country)
        return countries
    except Exception as e:
        print(f"Error fetching country of origin: {e}")
        return []

def fetch_awards_received(movie_uri):
    print(f"Fetching awards received for movie URI: {movie_uri}")
    uriid = movie_uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?award ?label WHERE {{
        wd:{uriid} wdt:P166 ?award .
        ?award rdfs:label ?label .
        FILTER(LANG(?label) = "en")
    }}
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        awards = []
        for binding in results["results"]["bindings"]:
            award = {
                "label": binding["label"]["value"],
                "uri": binding["award"]["value"]
            }
            awards.append(award)
        return awards
    except Exception as e:
        print(f"Error fetching awards received: {e}")
        return []

def fetch_filming_locations(movie_uri):
    print(f"Fetching filming locations for movie URI: {movie_uri}")
    uriid = movie_uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?location ?label ?image WHERE {{
        wd:{uriid} wdt:P915 ?location .
        ?location rdfs:label ?label .
        OPTIONAL {{ ?location wdt:P18 ?image. }}
        FILTER(LANG(?label) = "en")
    }}
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        locations = []
        for binding in results["results"]["bindings"]:
            location = {
                "label": binding["label"]["value"],
                "uri": binding["location"]["value"],
                "image": binding["image"]["value"] if "image" in binding else None
            }
            locations.append(location)
        return locations
    except Exception as e:
        print(f"Error fetching filming locations: {e}")
        return []