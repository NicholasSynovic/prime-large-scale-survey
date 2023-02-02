import subprocess
from io import TextIOWrapper
from json import dump
from pathlib import PurePath
from time import sleep
from typing import List
from urllib.parse import ParseResult, urlparse

import requests
from primeLSS import PrimeLSSElement
from progress.spinner import MoonSpinner as Spinner
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


def gitPing(url: str) -> int:
    parsedURL: ParseResult = urlparse(url)
    gitURL: str = f"git@github.com:{parsedURL.path.strip('/')}"

    command: List[str] = ["git", "ls-remote", "--exit-code", "-h", gitURL]

    return subprocess.run(
        args=command, shell=False, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    ).returncode


def buildElement(resp: Response, gitPingStatus: int) -> PrimeLSSElement:
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
        case 301:
            action = 1
        case _:
            action = 2

    return PrimeLSSElement(
        id=elementID,
        original_url=originalURL,
        new_url=newURL,
        original_url_status_code=originalStatusCode,
        action=action,
        repo_status=gitPingStatus,
    )


def main() -> None:
    outputFilePath: PurePath = PurePath("mergedURLs.json")

    stream: TextIOWrapper = open(file="test.txt", mode="r", buffering=1)
    streamIterable = map(str.strip, iter(stream.readline, ""))

    with Spinner("Resolving GitHub URLs... ") as spinner:
        url: str
        for url in streamIterable:
            spinner.message = f"Resolving {url}... "
            spinner.update()

            resp: Response = getURL(url)
            gitStatus: int = gitPing(url)
            p: PrimeLSSElement = buildElement(resp, gitPingStatus=gitStatus)
            jsonObjects.append(p.to_dict())
            spinner.next()

    print(f"Saving file to {outputFilePath}...")
    with open(file=outputFilePath, mode="w") as json:
        dump(obj=jsonObjects, fp=json)
        json.close()


if __name__ == "__main__":
    main()
