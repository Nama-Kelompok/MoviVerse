from .sparql import wikidata_sparql

def fetch_director_uri(uri, nama):
    """
    Fetch director URI from Wikidata using movie URI and director's name.
    """
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
            return None
    except Exception as e:
        print(f"Error fetching director URI for {nama}: {e}")
        return None
