from .sparql import wikidata_sparql

def fetch_crew_members(movie_uri, property_id):
    uriid = movie_uri.split("/")[-1] 
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?person ?label (SAMPLE(?image) AS ?image) WHERE {{
        wd:{uriid} wdt:{property_id} ?person .
        ?person rdfs:label ?label .
        OPTIONAL {{ ?person wdt:P18 ?image. }}
        FILTER(LANG(?label) = "en")
    }}
    GROUP BY ?person ?label
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        crew_members = []
        for binding in results["results"]["bindings"]:
            member = {
                "label": binding["label"]["value"],
                "uri": binding["person"]["value"],
                "image": binding["image"]["value"] if "image" in binding else None
            }
            crew_members.append(member)
        return crew_members
    except Exception as e:
        print(f"Error fetching crew members for property {property_id}: {e}")
        return []

def fetch_director_of_photography(movie_uri):
    return fetch_crew_members(movie_uri, 'P344')

def fetch_film_editor(movie_uri):
    return fetch_crew_members(movie_uri, 'P1040')

def fetch_production_designer(movie_uri):
    return fetch_crew_members(movie_uri, 'P2554')

def fetch_costume_designer(movie_uri):
    return fetch_crew_members(movie_uri, 'P2515')

def fetch_composer(movie_uri):
    return fetch_crew_members(movie_uri, 'P86')

def fetch_producer(movie_uri):
    return fetch_crew_members(movie_uri, 'P162')
