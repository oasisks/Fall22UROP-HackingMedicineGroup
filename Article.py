from bs4 import BeautifulSoup
import requests
import os


class Div:
    def __init__(self, div):
        self.div = div

    def paragraphs(self) -> list:
        """
        This returns a list of paragraph objects (if there are any)
        :return: list
        """

        return [html_element for html_element in self.div if html_element.name == 'p']


def _flatten(to_be_flatten, solution=None) -> list:
    """
    Flattens a list
    :param to_be_flatten: list
    :return: list
    """
    if solution is None:
        solution = []

    for element in to_be_flatten:
        if isinstance(element, list):
            _flatten(element, solution)
        else:
            solution.append(element)

    return solution


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

    def to_text_file(self) -> None:
        """
        Save the article in a .txt extension under the folder named Articles.
        If Articles do not exist, it will create an Article folder.
        :return: None
        """

        path = None
        try:
            # attempting to create a directory
            path = os.path.join(os.getcwd(), r'Articles')
            os.mkdir(path)
        except FileExistsError:
            print("/Article Already exists.")
        except FileNotFoundError:
            print("Path is Invalid")

        if path is not None:
            path = os.path.join(path, f'{self._url.split("/")[-1]}')
            file = open(path, "w", encoding="utf-8")

            for div in self.divs:
                file.writelines(_flatten([p.contents for p in div.paragraphs()]))

            file.close()

    def __str__(self):
        """
        It should return the html content of the page
        """

        return self._prettify


if __name__ == '__main__':
    url = "https://news.mit.edu/2022/methane-research-takes-new-urgency-mit-1102"
    article = Article(url)
    article.to_text_file()
    # print(article)
