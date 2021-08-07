import math
from collections import namedtuple
from typing import List

import requests
from bs4 import BeautifulSoup
import wget

# Book = namedtuple("Book", "Author Series Title Language File Number")


class Book:
    def __init__(self, author, series, title, language, file, number, links):
        self.author = author
        self.series = series
        self.title = title
        self.language = language
        self.file = file
        self.number = number
        self.links = links

    def __str__(self) -> str:
        return f"{self.title}"


def scrape(search, book_format="") -> List[Book]:
    """get all results from search"""

    # replace space with + in search
    search.replace(" ", "+")

    # base url used for searches
    params = {"q": search, "format": book_format}

    # parse website
    r = requests.get("http://gen.lib.rus.ec/fiction/?", params=params)

    soup = BeautifulSoup(r.text, "html.parser")

    # get number of results
    number_of_results = soup.find("div", {"class": "catalog_paginator"})

    # if there are no results return an empty list
    try:
        div_string = number_of_results.text.strip()
    except:
        return list()
    div_string = [int(s) for s in div_string.split() if s.isdigit()]
    number_of_results = div_string[0]

    # get number of pages from number of results
    number_of_pages = math.ceil(number_of_results / 25)

    # loop every page
    book_list = []
    links = []
    counter = 1

    for i in range(1, number_of_pages + 1):
        # base url used for searches

        params = {"q": search, "format": book_format, "page": i}

        # parse website
        r = requests.get("http://gen.lib.rus.ec/fiction/?", params=params)
        soup = BeautifulSoup(r.text, "html.parser")
        libgen_table = soup.find("table")
        table_body = libgen_table.find("tbody")

        # get links from website
        all_links = table_body.find_all("ul", {"class": "record_mirrors_compact"})
        for link in all_links:
            link_list = link.find_all("li")
            link = link_list[0].find("a")
            links.append(link.get("href"))

        # get table from page
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            cols.pop()  # remove edits
            cols.pop()  # remove Mirrors
            cols.append(counter)
            counter += 1
            book_meta = [ele for ele in cols]
            book = Book(*book_meta, links=links)
            book_list.append(book)

    return book_list


def download_book(link, dest):

    # parse website
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")

    # parse link
    link = soup.find_all("h2")
    link = link[0].find("a")
    link = link.get("href")

    # download
    wget.download(link, out=dest)


if __name__ == "__main__":
    search = "viriconium"
    book_format = "epub"

    book_list = scrape(search, book_format)

    for book in book_list:
        print(book)
