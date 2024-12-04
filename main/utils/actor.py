from .sparql import wikidata_sparql, local_sparql

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