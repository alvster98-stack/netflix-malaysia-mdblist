import os
import requests
from bs4 import BeautifulSoup

API_KEY = os.environ["MDBLIST_API_KEY"]

LIST_ID = "alvster98/netflix-malaysia"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def scrape_titles():

    url = "https://ottasia.com/whats-new/netflix/malaysia"

    html = requests.get(url, timeout=30).text

    soup = BeautifulSoup(html, "html.parser")

    titles = []

    for tag in soup.find_all(["h2", "h3"]):

        title = tag.get_text(strip=True)

        ignore = [
            "What's new",
            "Recently added",
            "Netflix in other countries",
            "other services"
        ]

        if title and not any(x in title for x in ignore):
            titles.append(title)

    return list(set(titles))


def mdblist_search(title):

    url = "https://api.mdblist.com/search"

    r = requests.get(
        url,
        headers=headers,
        params={"query": title}
    )

    if r.status_code != 200:
        print("Search failed:", title)
        return None

    results = r.json()

    if not results:
        return None

    item = results[0]

    return item.get("imdb_id")


def add_item(imdb_id):

    url = "https://api.mdblist.com/lists/add"

    data = {
        "list": LIST_ID,
        "items": [
            imdb_id
        ]
    }

    r = requests.post(
        url,
        headers=headers,
        json=data
    )

    print(r.status_code, r.text)


def main():

    titles = scrape_titles()

    print(
        "Found:",
        len(titles)
    )

    for title in titles:

        print(
            "Processing:",
            title
        )

        imdb = mdblist_search(title)

        if imdb:
            add_item(imdb)


if __name__ == "__main__":
    main()
