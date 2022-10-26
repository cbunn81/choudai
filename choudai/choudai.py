from pathlib import Path

import bs4
import requests


def get_elements(soup: bs4.BeautifulSoup, element: str) -> bs4.element.ResultSet:
    return soup.find_all(element)


def save_html(html: str, path: str) -> None:
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("w", encoding="utf-8") as f:
        f.write(html)


def get_soup(url: str) -> bs4.BeautifulSoup:
    session = requests.Session()
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # # print(soup.prettify("utf-8"))
    # tags_inner = {"img": "src", "link": "href", "script": "src"}
    # for element in html.find_all("img"):
    #     if element.has_attr("src"):
    #         print(url + element["src"])
    return soup


def main():
    url = "https://www.wikipedia.org/"
    soup = get_soup(url=url)
    # print(soup)
    print(type(soup))
    images = get_elements(soup=soup, element="img")
    print(type(images[0]))
    num_images = len(images)
    print(num_images)
    p = Path(".")
    print(type(p.resolve()))
    # save to file
    save_html(html=str(soup), path="tmp.html")


if __name__ == "__main__":
    main()
