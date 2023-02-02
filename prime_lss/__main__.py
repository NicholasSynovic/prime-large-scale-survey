import concurrent.futures
from time import sleep
from typing import List

import requests
from progress.spinner import Spinner
from requests import Response

from prime_lss.primeLSS import PrimeLSSElement

jsonObjects: List[dict] = []


def getURL(url: str) -> Response:
    while True:
        resp: Response = requests.get(url=url, allow_redirects=False)

        if resp.status_code == 429:
            sleep(secs=60)
        else:
            break

    return resp


def buildElement(resp: Response) -> PrimeLSSElement:
    action: int

    originalURL: str = resp.url
    elementID: int = hash(originalURL)
    originalStatusCode: int = resp.status_code
    newURL: str | None = resp.headers.get("Location")

    if newURL == None:
        newURL = originalURL

    match originalStatusCode:
        case 200:
            action = 0
        case 404:
            action = -1
        case _:
            action = 1

    return PrimeLSSElement(
        id=elementID,
        original_url=originalURL,
        new_url=newURL,
        original_url_status_code=originalStatusCode,
        action=action,
    )


def main() -> None:
    with open("largeurls.txt", "r") as stream:
        lines = stream.readlines()

    urls = [line.strip() for line in lines]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_url, url) for url in urls]

        concurrent.futures.wait(futures)

    fetch_url(url="https://github.com/SoftwareSystemsLaboratory/clime")


if __name__ == "__main__":
    main()
