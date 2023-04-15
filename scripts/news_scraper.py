import requests
from bs4 import BeautifulSoup
from news.models import Article


class NewsScrapper:
    URL = "https://theprint.in/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    categories = [
        "politics",
        "economy",
        "defence",
        "india",
        "diplomacy",
    ]

    pageLinks = []

    # scrapping article urls
    def article_urls(self):
        Links = []
        for category in self.categories:
            url = f"{self.URL}/category/{category}/"
            headers = self.HEADERS

            try:
                response = requests.get(url=url, headers=headers)
                soup = BeautifulSoup(response.content, "html5lib")
                page = soup.select("div.td-module-container.td-category-pos-image")
                Links.extend(
                    [
                        article.div.a["href"]
                        for article in page
                        if article.div.a["href"] not in self.pageLinks
                    ]
                )
            except requests.exceptions.RequestException as e:
                print(f"Error occured while accessing URL {url}: {e}")
        return Links

    def scrap_article(self):
        for url in self.article_urls():
            headers = self.HEADERS
            r = requests.get(url=url, headers=headers)

            try:
                soup = BeautifulSoup(r.content, "html5lib")

                heading = soup.find("h1", attrs={"class": "tdb-title-text"})

                time = soup.find(
                    "time", attrs={"class": "entry-date updated td-module-date"}
                )

                image = ""
                try:
                    figure = soup.find("figure")
                    if figure and "data-gmsrc" in figure.img.attrs:
                        image = figure.img["data-gmsrc"]
                except:
                    pass

                tags = soup.find("div", attrs={"class": "tdb-category td-fix-index"})
                all_tags = [tag.text for tag in tags.children]

                content = soup.find(
                    "div",
                    attrs={
                        "class": "td_block_wrap tdb_single_content tdi_83 td-pb-border-top td_block_template_8 td-post-content tagdiv-type"
                    },
                ).find_all("p")
                article = "".join(
                    [p.text for p in content if "Also read:" not in p.text]
                )

                # fill up data
                model_instance = Article()
                model_instance.heading = heading.text
                model_instance.time = time.text
                model_instance.image_url = image if image else ""
                model_instance.tags = all_tags
                model_instance.article = article
                model_instance.save()

            except requests.exceptions.RequestException as e:
                print(f"Error occurred while accessing URL {url}:{e}")


def run():
    news1 = NewsScrapper()
    news1.scrap_article()
