import datetime
import os
import time
import random

import bs4
import requests
from feedgen.feed import FeedGenerator
from tqdm import tqdm

HOME_DIR = "../static/rss/"  # Adjust to where you want the XML files saved

CATEGORIES = ['oikonomia', 'apopsi', 'politiki', 'diethni-themata', 'tehnologia', 'aytokinito', 'agores']  # Replace with actual category IDs or names

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

def fetch_article_content(article_url):
    """Fetch the content of a given article."""
    time.sleep(random.randint(15,25))
    page = requests.get(article_url, headers=headers)
    soup = bs4.BeautifulSoup(page.content, "html.parser")

    content_div = soup.select_one(".article__body")

    if content_div:
        # Remove ad placeholders and other unwanted tags
        for unwanted_tag in content_div.find_all("div", class_="mobd-placeholder"):
            unwanted_tag.decompose()

        # Convert relative image URLs to absolute URLs
        for img in content_div.find_all("img"):
            if not img["src"].startswith(("http://", "https://")):  # If it's a relative URL
                img["src"] = "https://liberal.gr" + img["src"]

        # Preserve formatting by adding newline characters between block elements
        for block_element in content_div.find_all(["p", "div"]):
            block_element.append("\n")

        return str(content_div)  # Convert the content div to a string to retain HTML

    return None

def fetch_and_generate_rss_for_category(category_id):
    url = f"https://liberal.gr/katigories/{category_id}"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")

    urls = {}

    for article in tqdm(soup.select("div.article")):
        title = article.select_one("div.article__title p").text
        article_url = "https://liberal.gr" + article.select_one("a")["href"]

        image_element = article.select_one("img.object-fit-cover")
        if image_element:
            image_url = image_element["src"]
        else:
            image_url = None  # or provide a default URL or simply continue

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
    fg.title(f"Liberal.gr - {category_id.capitalize()}")
    fg.author({"name": "Liberal.gr"})
    fg.link(href=f"https://liberal.gr/katigories/{category_id}", rel="alternate")
    fg.subtitle(f"Arthro apo Liberal.gr Katigorias {category_id}.")
    fg.link(href=f"{HOME_DIR}/liberal.gr/{category_id}.xml", rel="self")
    fg.language("el")

    # urls = dict(sorted(urls.items(), key=lambda item: item[1]["date"], reverse=True))

    # for link in tqdm(urls):
    #     content = fetch_article_content(urls[link]["url"])  # Fetch the entire article content
    #
    #     fe = fg.add_entry()
    #     fe.id(urls[link]["url"])
    #     fe.title(link)
    #     fe.link(href=urls[link]["url"])
    #     if content:
    #         fe.content(content, type='CDATA')
    #     else:
    #         fe.description(link)
    #     fe.pubDate(urls[link]["date"])
    #     fe.enclosure(url=urls[link]["image"], type="image/jpeg")

    fg.rss_file(os.path.join(HOME_DIR, f"liberal.gr/{category_id}.xml"))
    print(f"{category_id}.xml generated...")


for category in CATEGORIES:
    fetch_and_generate_rss_for_category(category)
