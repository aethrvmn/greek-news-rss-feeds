import datetime
import os

import bs4
import requests
from feedgen.feed import FeedGenerator

HOME_DIR = "liberal.gr/"  # Adjust to where you want the XML files saved

CATEGORIES = ['politiki', 'oikonomia']  # Replace with actual category IDs or names

def fetch_and_generate_rss_for_category(category_id):
    url = f"https://liberal.gr/katigories/{category_id}"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")

    urls = {}
    for article in soup.select("div.article"):
        title = article.select_one("div.article__title p").text
        article_url = "https://liberal.gr" + article.select_one("a")["href"]
        image_url = article.select_one("img.object-fit-cover")["src"]

        # Extracting and formatting the date
        date_parts = article.select_one("div.article__info").text.split("•")
        date_str = date_parts[0].strip()
        time_str = date_parts[1].strip() if len(date_parts) > 1 else "00:00"
        date = datetime.datetime.strptime(date_str + " " + time_str, "%d/%m/%Y %H:%M")
        date = date.strftime("%Y-%m-%dT%H:%M:%S") + "-08:00"

        urls[title] = {
            "url": article_url,
            "date": date,
            "image": image_url
        }

    fg = FeedGenerator()
    fg.id(f"https://liberal.gr/katigories/{category_id}")
    fg.title(f"Liberal.gr {category_id}")
    fg.author({"name": "Liberal.gr"})
    fg.link(href=f"https://liberal.gr/katigories/{category_id}", rel="alternate")
    fg.subtitle(f"Posts from Liberal.gr Category {category_id}.")
    fg.link(href=f"{HOME_DIR}/liberal_category_{category_id}.xml", rel="self")

    urls = dict(sorted(urls.items(), key=lambda item: item[1]["date"], reverse=True))

    for link in urls:
        fe = fg.add_entry()
        fe.id(urls[link]["url"])
        fe.title(link)
        fe.link(href=urls[link]["url"])
        fe.description(link)
        fe.pubDate(urls[link]["date"])
        fe.enclosure(url=urls[link]["image"], type="image/jpeg")

    fg.language("en")

    fg.rss_file(os.path.join(HOME_DIR, f"liberal_category_{category_id}.xml"))


for category in CATEGORIES:
    fetch_and_generate_rss_for_category(category)
