from .sparql import wikidata_sparql

def fetch_review_scores(movie_uri, imdb_rating=None):
    uriid = movie_uri.split("/")[-1]
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?reviewer ?reviewerLabel ?score WHERE {{
        wd:{uriid} p:P444 ?reviewStatement .
        ?reviewStatement ps:P444 ?score .
        OPTIONAL {{
            ?reviewStatement pq:P447 ?reviewer .
            ?reviewer rdfs:label ?reviewerLabel .
            FILTER(LANG(?reviewerLabel) = "en") 
        }}
    }}
    LIMIT 5
    """

    wikidata_sparql.setQuery(sparql_query)

    try:
        results = wikidata_sparql.query().convert()
        reviews = []
        for binding in results.get("results", {}).get("bindings", []):
            score_raw = binding.get("score", {}).get("value", "")
            
            reviewer_label = binding.get("reviewerLabel", {}).get("value", "Unknown Reviewer")
            reviewer_uri = binding.get("reviewer", {}).get("value", "#") 
            reviews.append({
                "reviewer_label": reviewer_label,
                "reviewer_uri": reviewer_uri,
                "score": score_raw
            })

        if imdb_rating is not None:
            imdb_uri = "http://www.wikidata.org/entity/Q37312"
            for review in reviews:
                if review['reviewer_uri'] == imdb_uri:
                    reviews.remove(review)
                    break
            reviews.append({
                "reviewer_label": "IMDb",
                "reviewer_uri": imdb_uri,
                "score": imdb_rating
            })
                
        return reviews

    except Exception as e:
        print(f"Error fetching review scores: {e}")
        return []