import os
import time
import requests
from bs4 import BeautifulSoup

TMDB_KEY = os.environ["TMDB_API_KEY"]
MDBLIST_KEY = os.environ["MDBLIST_API_KEY"]

# Keep this for now until we confirm MDBList list endpoint format
MDBLIST_LIST = "alvster98/netflix-malaysia"


def scrape():

    url = "https://ottasia.com/whats-new/netflix/malaysia"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    ignore = [
        "What's new",
        "Recently added",
        "Netflix in other countries",
        "other services",
        "Netflixin other countries"
    ]

    titles = []

    for item in soup.find_all(["h2", "h3"]):

        title = item.get_text(strip=True)

        if title and not any(
            x.lower() in title.lower()
            for x in ignore
        ):
            titles.append(title)

    return list(set(titles))


def tmdb_search(title):

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

        if result.get("media_type") in ["movie", "tv"]:

            return {
                "id": result["id"],
                "type": result["media_type"],
                "title": title
            }

    return None


def add_to_mdblist(item):

    url = "https://api.mdblist.com/items/add"

    payload = {
        "list": MDBLIST_LIST,
        "items": [
            {
                "tmdb_id": item["id"],
                "media_type": item["type"]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {MDBLIST_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    print(
        "MDBList:",
        item["title"],
        response.status_code,
        response.text
    )


def main():

    titles = scrape()

    print(
        "Found titles:",
        len(titles)
    )

    for title in titles:

        result = tmdb_search(title)

        if result:

            print(
                "TMDB:",
                result
            )

            add_to_mdblist(result)

            time.sleep(2)

        else:

            print(
                "No TMDB match:",
                title
            )


if __name__ == "__main__":
    main()
