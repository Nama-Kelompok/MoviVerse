from .sparql import wikidata_sparql

def fetch_review_scores(movie_uri, limit=8):
    sparql_query = f"""
    PREFIX : <http://nama-kelompok.org/data/>
    PREFIX v: <http://nama-kelompok.org/vocab#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?reviewer ?reviewerLabel ?score WHERE {{
        <{movie_uri}> v:reviewScore ?score .
        <{movie_uri}> v:reviewer ?reviewer .
        ?reviewer rdfs:label ?reviewerLabel .
    }}
    LIMIT {limit}
    """

    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        reviews = []
        for binding in results["results"]["bindings"]:
            reviewer_uri = binding["reviewer"]["value"]
            reviewer_label = binding["reviewerLabel"]["value"]
            score = binding["score"]["value"]
            reviews.append({
                "reviewer_label": reviewer_label,
                "reviewer_uri": reviewer_uri,
                "score": score
            })
        return reviews
    except Exception as e:
        print(f"Error fetching review scores: {e}")
        return []