import requests
import json
from bs4 import BeautifulSoup
import os


TMDB_KEY = os.environ.get("TMDB_API_KEY")

if not TMDB_KEY:
    raise Exception("TMDB_API_KEY is missing")


def get_netflix_titles():

    url = "https://ottasia.com/whats-new/netflix/malaysia"

    response = requests.get(
        url,
        timeout=30
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    ignore = [
        "What's new",
        "Recently added",
        "Netflix in other countries",
        "Netflixin other countries",
        "other services"
    ]

    titles = []

    for item in soup.find_all(["h2", "h3"]):

        title = item.get_text(strip=True)

        if title and not any(
            bad.lower() in title.lower()
            for bad in ignore
        ):
            titles.append(title)

    return list(set(titles))


def find_tmdb(title):

    url = "https://api.themoviedb.org/3/search/multi"

    params = {
        "api_key": TMDB_KEY,
        "query": title
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    data = response.json()

    if "results" not in data:
        return None


    for result in data["results"]:

        if result.get("media_type") in [
            "movie",
            "tv"
        ]:

            return {
                "title": title,
                "tmdb_id": result["id"],
                "type": result["media_type"]
            }


    return None



def main():

    titles = get_netflix_titles()

    print("Found titles:", len(titles))


    catalog = []


    for title in titles:

        print("Searching:", title)

        item = find_tmdb(title)


        if item:

            print("Added:", item)

            catalog.append(item)

        else:

            print("No match:", title)



    movies = {
        "metas": []
    }

    series = {
        "metas": []
    }


    for item in catalog:

        meta = {
            "id": f"tmdb:{item['tmdb_id']}",
            "type": item["type"],
            "name": item["title"]
        }


        if item["type"] == "movie":

            movies["metas"].append(meta)


        elif item["type"] == "tv":

            meta["type"] = "series"

            series["metas"].append(meta)



    os.makedirs(
        "catalog/movie",
        exist_ok=True
    )

    os.makedirs(
        "catalog/series",
        exist_ok=True
    )



    with open(
        "catalog/movie/netflix-malaysia.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            movies,
            file,
            indent=2,
            ensure_ascii=False
        )



    with open(
        "catalog/series/netflix-malaysia.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            series,
            file,
            indent=2,
            ensure_ascii=False
        )


    print(
        "MOVIES:",
        len(movies["metas"])
    )

    print(
        "SERIES:",
        len(series["metas"])
    )


if __name__ == "__main__":
    main()
