import pandas as pd
import requests
import json
import os

def generate_url(title: str, paging: int):
    title = title.replace(" ", "%20")
    title = title.replace(":", "%3A")
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={title}&format=json&errorformat=plaintext&language=en&uselang=en&type=item"

    if paging == 0:
        return url
    else:
        return url + f"&continue={paging}"

if not os.path.exists("imdb_top_100_with_wikidata.csv"):
    df = pd.read_csv('imdb_top_1000.csv')
    titles = df['Series_Title']
    new_df = df.copy(True)
    new_df["wikidata_id"] = None

    for i, title in enumerate(titles):
        paging = 0
        url = generate_url(title, paging) #First paging
        r = requests.get(url)
        data = json.loads(r.text)
        search = data["search"]
        id = None

        if len(search) == 1 and "film" in search[0]["description"]:
            id = search[0]["id"]
        else:
            isExit = False
            while True:
                for movie in search:
                    movie["label"] = movie["label"].replace("\u2013", "-").replace(":", "").capitalize()

                    if "description" not in movie:
                        continue

                    if "film" in movie["description"]:
                        standarized_title = title.replace(":", "").capitalize()
                        if standarized_title == movie["label"]:
                            isExit = True
                            id = movie["id"]
                            break
                        elif "aliases" in movie:
                            movie["aliases"] = [x.replace("\u2013", "-").replace(":", "").capitalize() for x in movie["aliases"]]
                            if standarized_title in movie["aliases"]:
                                isExit = True
                                id = movie["id"]
                                break

                if "search-continue" not in data:
                    break

                if isExit:
                    break

                paging += 7
                url = generate_url(title, paging)
                r = requests.get(url)
                data = json.loads(r.text)
                search = data["search"]

        print(f"{i}. {title}: {id}")
        new_df.loc[i, "wikidata_id"] = id

    new_df.to_csv('imdb_top_100_with_wikidata.csv', index=False)

if not os.path.exists("highest_holywood_grossing_movies_with_wikidata.csv"):
    df = pd.read_csv('highest_holywood_grossing_movies.csv')
    titles = df['Title']
    new_df = df.copy(True)
    new_df["wikidata_id"] = None

    for i, title in enumerate(titles):
        paging = 0
        url = generate_url(title, paging) #First paging
        r = requests.get(url)
        data = json.loads(r.text)
        search = data["search"]
        id = None

        if len(search) == 1 and "film" in search[0]["description"]:
            id = search[0]["id"]
        else:
            isExit = False
            while True:
                for movie in search:
                    movie["label"] = movie["label"].replace("\u2013", "-").replace(":", "").capitalize()

                    if "description" not in movie:
                        continue

                    if "film" in movie["description"]:
                        standarized_title = title.replace(":", "").capitalize()
                        if standarized_title == movie["label"]:
                            isExit = True
                            id = movie["id"]
                            break
                        elif "aliases" in movie:
                            movie["aliases"] = [x.replace("\u2013", "-").replace(":", "").capitalize() for x in movie["aliases"]]
                            if standarized_title in movie["aliases"]:
                                isExit = True
                                id = movie["id"]
                                break

                if "search-continue" not in data:
                    break

                if isExit:
                    break

                paging += 7
                url = generate_url(title, paging)
                r = requests.get(url)
                data = json.loads(r.text)
                search = data["search"]

        print(f"{i}. {title}: {id}")
        new_df.loc[i, "wikidata_id"] = id

    new_df.to_csv('highest_holywood_grossing_movies_with_wikidata.csv', index=False)
