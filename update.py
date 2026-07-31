import os
import requests
from bs4 import BeautifulSoup

MDBLIST_API_KEY = os.environ["MDBLIST_API_KEY"]

USERNAME = "alvster98"
LIST_NAME = "netflix-malaysia"

HEADERS = {
    "Authorization": f"Bearer {MDBLIST_API_KEY}",
    "Content-Type": "application/json"
}


def get_netflix_malaysia_titles():
    url = "https://ottasia.com/whats-new/netflix/malaysia"

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    titles = []

    for item in soup.select("h3, h2"):
        title = item.get_text(strip=True)

        if title:
            titles.append(title)

    return list(set(titles))


def search_mdblist(title):
    url = "https://api.mdblist.com/search"

    params = {
        "query": title
    }

    r = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30
    )

    if r.status_code != 200:
        return None

    data = r.json()

    if not data:
        return None

    item = data[0]

    return {
        "mediatype": item.get("mediatype"),
        "id": item.get("imdb_id")
    }


def add_to_list(item):

    url = "https://api.mdblist.com/list/add"

    payload = {
        "username": USERNAME,
        "list": LIST_NAME,
        "items": [
            item
        ]
    }

    r = requests.post(
        url,
        headers=HEADERS,
        json=payload
    )

    print(r.text)


def main():

    titles = get_netflix_malaysia_titles()

    print(
        f"Found {len(titles)} Netflix Malaysia titles"
    )

    for title in titles:

        print(
            "Processing:",
            title
        )

        item = search_mdblist(title)

        if item:
            add_to_list(item)


if __name__ == "__main__":
    main()
