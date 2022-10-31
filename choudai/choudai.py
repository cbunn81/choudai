from pathlib import Path
from urllib.parse import urljoin

import bs4
import requests


def get_elements(soup: bs4.BeautifulSoup, element: str) -> bs4.element.ResultSet:
    return soup.find_all(element)


def download_assets(
    session: requests.sessions.Session,
    soup: bs4.BeautifulSoup,
    ref_map: dict[str, str],
    url: str,
    path: str,
) -> None:
    download_path = Path(path)
    download_path.mkdir(parents=True, exist_ok=True)
    for tag, ref in ref_map.items():
        elements = soup.find_all(tag)
        for element in elements:
            if element.has_attr(ref):
                filename = Path(element[ref]).name
                fileurl = urljoin(url, element[ref])
                filepath = download_path / filename
                element[ref] = str(download_path / filename)
                with open(filepath, "wb") as f:
                    f.write(session.get(fileurl).content)


def save_html(html: str, path: str) -> None:
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("w", encoding="utf-8") as f:
        f.write(html)


def get_soup(session: requests.sessions.Session, url: str) -> bs4.BeautifulSoup:
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return soup


def main():
    url = "https://www.wikipedia.org/"
    # map the elements we want to download byt tag with their reference identifiers
    ref_map = {"img": "src", "link": "href", "script": "src"}

    session = requests.Session()
    soup = get_soup(session=session, url=url)

    num_links = len(get_elements(soup=soup, element="a"))
    num_images = len(get_elements(soup=soup, element="img"))
    print(f"Site: {url}")
    print(f"Number of links: {num_links}")
    print(f"Number of images: {num_images}")
    download_assets(
        session=session,
        soup=soup,
        ref_map=ref_map,
        url=url,
        path="www.wikipedia.org_files",
    )
    # save to file
    save_html(html=str(soup), path="www.wikipedia.org.html")


if __name__ == "__main__":
    main()
