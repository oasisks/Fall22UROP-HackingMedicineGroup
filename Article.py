from bs4 import BeautifulSoup
import requests


class Div:
    def __init__(self, div):
        self.div = div

    def paragraphs(self) -> list:
        """
        This returns a list of paragraph objects (if there are any)
        :return: list
        """

        return [html_element for html_element in self.div if html_element.name == 'p']


class Article:
    def __init__(self, url):
        self._url = url

        _request = requests.get(url)
        self._soup = BeautifulSoup(_request.content, "html.parser")
        self._prettify = self._soup.prettify()

        look_for = {"class": "paragraph paragraph--type--content-block-text paragraph--view-mode--default"}

        self.divs = [Div(div) for div in self._soup.findAll("div", look_for)]

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

    for div in article.divs:
        print(div.paragraphs())
    # print(article)
