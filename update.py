import os
import requests
from bs4 import BeautifulSoup
MDBLIST_KEY = os.environ["MDBLIST_API_KEY"]
MDBLIST_LIST = "alvster98/netflix-malaysia"
TMDB_KEY = os.environ["TMDB_API_KEY"]
print("MDBLIST key loaded:", bool(MDBLIST_KEY))
print("MDBLIST key length:", len(MDBLIST_KEY))

titles = []
def add_to_mdblist(item):

    url = "https://api.mdblist.com/items/add"

    data = {
        "items": [
            {
                "tmdb_id": item["id"],
                "media_type": item["type"]
            }
        ],
        "list": MDBLIST_LIST
    }

    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {MDBLIST_KEY}",
            "Content-Type": "application/json"
        },
        json=data
    )

    print(r.status_code, r.text)

def scrape():

    url = "https://ottasia.com/whats-new/netflix/malaysia"

    soup = BeautifulSoup(
        requests.get(url).text,
        "html.parser"
    )

    ignore = [
        "What's new",
        "Recently added",
        "Netflix in other countries",
        "other services"
    ]

    for x in soup.find_all(["h2","h3"]):

        t = x.get_text(strip=True)

        if t and not any(i in t for i in ignore):
            titles.append(t)

    return list(set(titles))


def tmdb_search(title):

    url = "https://api.themoviedb.org/3/search/multi"

    params = {
        "api_key": TMDB_KEY,
        "query": title
    }

    r = requests.get(
        url,
        params=params
    )

    data = r.json()

    if data.get("results"):
        item = data["results"][0]

        return {
            "id": item["id"],
            "type": item["media_type"]
        }

    return None


def main():

    items = scrape()

    print("Found", len(items))

    for title in items:

        result = tmdb_search(title)

        if result:

            print(
                title,
                "→",
                result
            )

            add_to_mdblist(result)

        else:

            print(
                "No match:",
                title
            )


main()
