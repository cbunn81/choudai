import csv
import fileinput
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import bs4
import requests
import typer
import validators


def show_results(results: dict) -> None:
    for key, value in results.items():
        print(f"{key}: {value}")


def get_stored_results_from_csv(csvfile: str, url: str) -> dict:
    """Retrieve stored metadata results from a CSV file.
    Args:
        csvfile (str): A CSV file containing metadata results.
        url (str): The URL of the web page stored.
    Returns:
        dict: The results in a dictionary, if any.
    """
    csvfilepath = Path(csvfile).resolve()
    with open(csvfilepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["url"] == url:
                return row


def store_result_in_csv(
    csvfile: str, url: str, num_images: int, num_links: int
) -> None:
    """Store a web page download result in a given csvfile, creating the file if needed.
    Args:
        csvfile (str): The CSV file to use or create.
        url (str): The URL of the web page stored.
        num_images (int): The number of image tags on the page.
        num_links (int): The number of link tags on the page.
    """
    csvfilepath = Path(csvfile).resolve()
    csvfilepath.parent.mkdir(parents=True, exist_ok=True)
    # check if the CSV file already exists
    file_exists = csvfilepath.is_file()
    with open(csvfilepath, "a", newline="") as csvfile:
        fieldnames = ["url", "num_images", "num_links", "last_fetch"]

        # The last fetch datetime should be when this call to store the data is made
        last_fetch = datetime.now()

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # write the header if this is a new file to be created
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "url": url,
                "num_images": num_images,
                "num_links": num_links,
                "last_fetch": last_fetch,
            }
        )


def update_result_in_csv(
    csvfile: str, url: str, num_images: int, num_links: int
) -> None:
    """Store a web page download result in a given csvfile, creating the file if needed.
    Args:
        csvfile (str): The CSV file to use or create.
        url (str): The URL of the web page stored.
        num_images (int): The number of image tags on the page.
        num_links (int): The number of link tags on the page.
    """
    csvfilepath = Path(csvfile).resolve()
    # The last fetch datetime should be when this call to store the data is made
    last_fetch = datetime.now()

    with fileinput.input(files=csvfilepath, inplace=True, mode="r") as f:
        reader = csv.DictReader(f)
        print(",".join(reader.fieldnames))
        for row in reader:
            if row["url"] == url:
                row["num_images"] = num_images
                row["num_links"] = num_links
                row["last_fetch"] = last_fetch
            print(",".join(map(str, row.values())))


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


def fetch(url: str, csvfile: str) -> None:
    # map the elements we want to download by tag with their reference identifiers
    ref_map = {"img": "src", "link": "href", "script": "src"}

    if not validators.url(url):
        print(f"{url} is not a valid URL. Please enter valid URLs.")
        raise typer.Abort()

    session = requests.Session()
    soup = get_soup(session=session, url=url)

    site = urlparse(url=url).netloc

    num_links = len(get_elements(soup=soup, element="a"))
    num_images = len(get_elements(soup=soup, element="img"))
    download_assets(
        session=session,
        soup=soup,
        ref_map=ref_map,
        url=url,
        path=f"/data/{site}_files",
    )

    # save HTML to file
    filename = f"/data/{site}.html"
    save_html(html=str(soup), path=filename)

    # Check if a result already exists for the URL
    csvfilepath = Path(csvfile).resolve()
    csvfilepath.parent.mkdir(parents=True, exist_ok=True)
    # check if the CSV file already exists
    if csvfilepath.is_file() and get_stored_results_from_csv(csvfile=csvfile, url=url):
        update_result_in_csv(
            csvfile=csvfile, url=url, num_images=num_images, num_links=num_links
        )
    else:
        # Save metadata to file
        store_result_in_csv(
            csvfile=csvfile, url=url, num_images=num_images, num_links=num_links
        )


def main(urls: list[str], metadata: bool = False):

    # CSV file for metadata storage
    csvfile = "/data/choudai-results.csv"

    for url in urls:
        if not metadata:
            # fetch web page and store results
            fetch(url=url, csvfile=csvfile)
        else:
            # get stored results
            results = get_stored_results_from_csv(csvfile=csvfile, url=url)
            if not results:
                print(f"There are no results stored for {url}")
            else:
                show_results(results=results)


if __name__ == "__main__":
    typer.run(main)
