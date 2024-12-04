from .sparql import wikidata_sparql

def fetch_all_screenwriters(movie_uri):
    uriid = movie_uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier#>
    
    SELECT DISTINCT ?screenwriter ?label ?image WHERE {{
        wd:{uriid} p:P58 ?screenwriterStatement .
        ?screenwriterStatement ps:P58 ?screenwriter .
        OPTIONAL {{ ?screenwriter wdt:P18 ?image. }}
        ?screenwriter rdfs:label ?label .
        FILTER(LANG(?label) = "en")
    }}
    """
    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        screenwriters = []
        for binding in results["results"]["bindings"]:
            screenwriter = {
                "label": binding["label"]["value"],
                "uri": binding["screenwriter"]["value"],
                "image": binding["image"]["value"] if "image" in binding else None
            }
            screenwriters.append(screenwriter)
        return screenwriters
    except Exception as e:
        print(f"Error fetching all screenwriters: {e}")
        return []
