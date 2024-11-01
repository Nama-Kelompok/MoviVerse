import pandas as pd
import os
from SPARQLWrapper import SPARQLWrapper, JSON

df = pd.read_csv('imdb_top_1000.csv')
selected_df = df[['Series_Title', 'Released_Year']]
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

new_df = df.copy(True)
new_df["wikidata_id"] = None

start_len = None
if not os.path.exists("imdb_top_1000_with_wikidata.csv"):
    new_df[0:0].to_csv("imdb_top_1000_with_wikidata.csv", index=False)
    start_len = 0
else:
    temp_df = pd.read_csv('imdb_top_1000_with_wikidata.csv')
    start_len = len(temp_df)
    print(temp_df)

if start_len <= 999:
    for i in range(start_len, 1000):
        rows = selected_df.iloc[i]
        title = rows["Series_Title"]
        year = rows["Released_Year"]

        if year.isdigit():
            sparql.setQuery(f"""
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                SELECT DISTINCT ?id where {{
                  ?id wdt:P31 wd:Q11424 .
                  ?id rdfs:label ?filmlabel .
                  ?id wdt:P577 ?releasedate .
                  FILTER (REGEX(?filmlabel, "^{title}$", "i")) .
                  FILTER (YEAR(?releasedate) = {year}) .
                }}
            """)
        else:
            sparql.setQuery(f"""
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                SELECT DISTINCT ?id where {{
                  ?id wdt:P31 wd:Q11424 .
                  ?id rdfs:label ?filmlabel .
                  ?id wdt:P577 ?releasedate .
                  FILTER (REGEX(?filmlabel, "^{title}$", "i")) .
                }}
            """)

        result: str = None
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            result = results["results"]["bindings"][0]["id"]["value"]

        print(f"{i}. {title} : {result}")
        new_df.loc[i, "wikidata_id"] = result

        if (i + 1) % 10 == 0:
            new_df[i-9:i+1].to_csv('imdb_top_1000_with_wikidata.csv', mode='a', header=False, index=False)

df = pd.read_csv('highest_holywood_grossing_movies.csv')
selected_df = df[['Title', 'Year']]
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

new_df = df.copy(True)
new_df["wikidata_id"] = None

start_len = None
if not os.path.exists("highest_holywood_grossing_movies_with_wikidata.csv"):
    new_df[0:0].to_csv("highest_holywood_grossing_movies_with_wikidata.csv", index=False)
    start_len = 0
else:
    temp_df = pd.read_csv('highest_holywood_grossing_movies_with_wikidata.csv')
    start_len = len(temp_df)
    print(temp_df)

if start_len <= 999:
    for i in range(start_len, 1000):
        rows = selected_df.iloc[i]
        title = rows["Title"]
        year = rows["Year"]

        if year is not None:
            sparql.setQuery(f"""
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                SELECT DISTINCT ?id where {{
                  ?id wdt:P31 wd:Q11424 .
                  ?id rdfs:label ?filmlabel .
                  ?id wdt:P577 ?releasedate .
                  FILTER (REGEX(?filmlabel, "^{title}$", "i")) .
                  FILTER (YEAR(?releasedate) = {year}) .
                }}
            """)
        else:
            sparql.setQuery(f"""
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                SELECT DISTINCT ?id where {{
                  ?id wdt:P31 wd:Q11424 .
                  ?id rdfs:label ?filmlabel .
                  ?id wdt:P577 ?releasedate .
                  FILTER (REGEX(?filmlabel, "^{title}$", "i")) .
                }}
            """)

        result: str = None
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            result = results["results"]["bindings"][0]["id"]["value"]

        print(f"{i}. {title} : {result}")
        new_df.loc[i, "wikidata_id"] = result

        if (i + 1) % 10 == 0:
            new_df[i-9:i+1].to_csv('highest_holywood_grossing_movies_with_wikidata.csv', mode='a', header=False, index=False)
