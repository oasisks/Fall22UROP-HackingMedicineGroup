from bs4 import BeautifulSoup
import requests


class Article:
    def __init__(self, url):
        self._url = url

        _request = requests.get(url)
        self._soup = BeautifulSoup(_request.content, "html.parser")
        self._prettify = self._soup.prettify()

        look_for = {"class": "paragraph paragraph--type--content-block-text paragraph--view-mode--default"}
        for div in self._soup.findAll("div", look_for):
            pass


    def get_url(self):
        """
        Returns the url of the article
        :return: str
        """
        return self._url

    def __str__(self):
        """
        It should return the html content of the page
        """

        return self._prettify


if __name__ == '__main__':
    url = "https://news.mit.edu/2022/methane-research-takes-new-urgency-mit-1102"
    article = Article(url)

    # print(article)
