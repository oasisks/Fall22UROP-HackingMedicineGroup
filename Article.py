from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


class Div:
    def __init__(self, div):
        self.div = div

    def paragraphs(self) -> list:
        """
        This returns a list of paragraph texts (if there are any)
        :return: list
        """

        def all_contents(tag) -> str:
            """
            A helper function that recursively returns all the contents as a string
            :param tag: list
            :return: str
            """

            content = ""
            for element in tag:
                if isinstance(element, str):
                    content += element
                else:
                    content += all_contents(element.contents)

            return content

        return [all_contents(html_element.contents) for html_element in self.div if html_element.name == 'p']

    def list_elements(self) -> list:
        """
        Returns all list items under this specific div
        :return: list
        """
        li_tags = self.div.find_all("li", href=True)

        for tag in li_tags:
            print("hello")
            print(tag['href'])


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
        """
        self.paragraphs: Div
        self.related_links: Div
        self.related_topics: Div
        """
        self._url = url

        _request = requests.get(url)
        self._soup = BeautifulSoup(_request.content, "html.parser")
        self._prettify = self._soup.prettify()

        self.contents = {"paragraphs":
                             {"class": "paragraph paragraph--type--content-block-text paragraph--view-mode--default"},
                         "related_links":
                             {"class": "news-article--content--related-links"},
                         "related_topics":
                             {"class": "news-article--topics"}}

        self.contents = {topic: [Div(div) for div in self._soup.find_all("div", look_for)]
                         for topic, look_for in self.contents.items()}

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
            path = os.path.join(path, f'{self._url.split("/")[-1]}.txt')
            file = open(path, "w", encoding="utf-8")

            for div in self.contents["paragraphs"]:
                file.write("\n".join(div.paragraphs()))

            file.close()

    def to_dataframe(self, csv=True) -> pd.DataFrame:
        """
        Converts relevant data into a dataframe
        :param csv: bool
        :return: pd.DataFrame
        """

    def __str__(self):
        """
        It should return the html content of the page
        """

        return self._prettify


if __name__ == '__main__':
    url = "https://news.mit.edu/2022/methane-research-takes-new-urgency-mit-1102"
    article = Article(url)

    print(article.contents["related_links"][0].list_elements())
    