import pandas as pd
import requests
import json

def generate_url(title: str, paging: int):
    title = title.replace(" ", "%20")
    title = title.replace(":", "%3A")
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={title}&format=json&errorformat=plaintext&language=en&uselang=en&type=item"

    if paging == 0:
        return url
    else:
        return url + f"&continue={paging}"



df = pd.read_csv('imdb_top_1000.csv')
titles = df['Series_Title']

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
                movie["label"] = movie["label"].replace("\u2013", "-").replace(":", "")

                if "description" not in movie:
                    continue

                if "film" in movie["description"]:
                    if title.replace(":", "") == movie["label"]:
                        isExit = True
                        id = movie["id"]
                        break
                    elif "aliases" in movie and title.replace(":", "") in movie["aliases"]:
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


    print(f"{title}: {id}")
    if i == 100:
        break
