from .sparql import wikidata_sparql

def fetch_image(uri):
    sparql_query = f"""
    SELECT ?image WHERE {{
        BIND(<{uri}> AS ?entity) .
        ?entity wdt:P18 ?image .
    }}
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["image"]["value"]
        else:
            return None
    except Exception as e:
        print(f"Error fetching image for {uri}: {e}")
        return None
