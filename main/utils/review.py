# utils/review.py

from .sparql import wikidata_sparql

def fetch_review_scores(movie_uri):
    print(movie_uri)
    sparql_query = f"""
    PREFIX : <http://nama-kelompok.org/data/>
    PREFIX v: <http://nama-kelompok.org/vocab#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?reviewer ?reviewerLabel ?score WHERE {{
        <{movie_uri}> v:P444 ?score .
        <{movie_uri}> v:P447 ?reviewer .
        ?reviewer rdfs:label ?reviewerLabel .
    }}
    LIMIT 8
    """

    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        print(results)

        reviews = []
        for binding in results.get("results", {}).get("bindings", []):
            reviewer_uri = binding.get("reviewer", {}).get("value")
            reviewer_label = binding.get("reviewerLabel", {}).get("value")
            score = binding.get("score", {}).get("value")

            # Pastikan semua data tersedia
            if reviewer_uri and reviewer_label and score:
                reviews.append({
                    "reviewer_label": reviewer_label,
                    "reviewer_uri": reviewer_uri,
                    "score": score
                })

        return reviews

    except Exception as e:
        print(f"Error fetching review scores: {e}")
        return []
