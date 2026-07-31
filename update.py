import requests
import json
from bs4 import BeautifulSoup
import os

TMDB_KEY = os.environ["TMDB_API_KEY"]


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

    if data.get("results"):

        result = data["results"][0]

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

    print(
        "Found:",
        len(titles)
    )

    catalog = []


    for title in titles:

        print(
            "Searching:",
            title
        )

        item = find_tmdb(title)

        if item:

            print(
                "Added:",
                item
            )

            catalog.append(item)

        else:

            print(
                "No TMDB match:",
                title
            )


    stremio_catalog = {
        "metas": []
    }


    for item in catalog:

        stremio_catalog["metas"].append(
            {
                "id": f"{item['type']}:{item['tmdb_id']}",
                "type": item["type"],
                "name": item["title"]
            }
        )


    with open(
        "netflix-malaysia.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            stremio_catalog,
            file,
            indent=2,
            ensure_ascii=False
        )


    with open(
        "catalog.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            stremio_catalog,
            file,
            indent=2,
            ensure_ascii=False
        )


    print(
        "Created catalog:",
        len(catalog),
        "titles"
    )


if __name__ == "__main__":
    main()
