from bs4 import BeautifulSoup
from imdb_helper_functions import *
import urllib


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    if not isinstance(cast_page_soup, BeautifulSoup):
        raise Exception("cast_page_soup is not BeautifulSoup obj")
    if num_of_actors_limit is not None:
        if not isinstance(num_of_actors_limit, int) or num_of_actors_limit < 1:
            raise Exception("num_of_actors_limit is not positive int")

    tr_arr = cast_page_soup.find("table", attrs={"class": "cast_list"}).find_all("tr", attrs={"class": ["even", "odd"]})

    result = []
    for tr in tr_arr:
        td = tr.find("td", attrs={"class": ""})
        name_of_actor, url_to_actor_page = td.text.strip(), urllib.parse.urljoin("https://www.imdb.com", td.find("a")["href"])
        result.append((name_of_actor, url_to_actor_page))

    return result[:num_of_actors_limit] if num_of_actors_limit else result


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    if not isinstance(actor_page_soup, BeautifulSoup):
        raise Exception("actor_page_soup is not BeautifulSoup obj")
    if num_of_movies_limit is not None:
        if not isinstance(num_of_movies_limit, int) or num_of_movies_limit < 1:
            raise Exception("num_of_movies_limit is not positive int")

    excluded_types = set(("TV Series", "Short", "Video Game", "Video short", "Video", "TV Movie", "TV Mini-Series",
                          "TV Series short", "TV Special"))

    div_arr = actor_page_soup.select("div#filmography div.filmo-category-section div[id^='act']")

    result = []
    for div in div_arr:
        if div.select_one("a.in_production"):
            continue
        if "(" in div.text:
            if div.text[div.text.index("(") + 1:div.text.index(")")] in excluded_types:
                continue

        a = div.select_one("b>a")
        name_of_movie, url_to_movie_page = a.text, urllib.parse.urljoin("https://www.imdb.com", a["href"])
        result.append((name_of_movie, url_to_movie_page))

    return result[:num_of_movies_limit] if num_of_movies_limit else result
