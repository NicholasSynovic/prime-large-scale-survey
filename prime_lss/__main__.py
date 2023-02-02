from concurrent.futures import ThreadPoolExecutor
from io import TextIOWrapper
from json import dump
from time import sleep
from typing import List

import requests
from primeLSS import PrimeLSSElement
from progress.spinner import Spinner
from requests import Response

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


def concurrentEvaluation(streamIterable: map) -> None:
    with Spinner("Resolving GitHub URLs...") as spinner:

        def _helper(url: str) -> None:
            resp: Response = getURL(url)
            p: PrimeLSSElement = buildElement(resp)
            jsonObjects.append(p.to_dict())
            spinner.next()

        with ThreadPoolExecutor() as executor:
            executor.map(_helper, streamIterable)


def main() -> None:

    stream: TextIOWrapper = open(file="mergedURLs.txt", mode="r", buffering=1)
    streamIterable = map(str.strip, iter(stream.readline, ""))

    concurrentEvaluation(streamIterable=streamIterable)

    with open(file="outputURLs.json", mode="w") as json:
        dump(obj=jsonObjects, fp=json)
        json.close()


if __name__ == "__main__":
    main()
