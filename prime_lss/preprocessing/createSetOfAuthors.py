from concurrent.futures import ThreadPoolExecutor
from io import TextIOWrapper
from pathlib import PurePath
from typing import List
from urllib.parse import ParseResult, urlparse

import cardinality
from progress.bar import Bar


def repoToAuthorURLConversion(url: str) -> str:
    author: str
    parsedURL: ParseResult = urlparse(url)
    strippedPath: str = parsedURL.path.strip("/")
    splitPath: List[str] = strippedPath.split("/")

    if splitPath[0] == "":
        try:
            author = splitPath[1]
        except IndexError:
            author = ""

    author = splitPath[0]
    return f"https://github.com/{author}\n"


def main() -> None:
    #     authorURLs: List[str] = []
    authorURLs: set[str] = set()
    inputFilepath: PurePath = PurePath("/mnt/c/Users/nicho/Desktop/mergedURLs.txt")
    outputFilepath: PurePath = PurePath(
        "/mnt/c/Users/nicho/Desktop/setOfAuthorURLs.txt"
    )

    stream: TextIOWrapper = open(file=inputFilepath, mode="r", buffering=1)
    streamIterable: map = map(str.strip, iter(stream.readline, ""))

    with Bar(
        "Converting GitHub Repo URLs to GitHub Author URLs (estimated length)... ",
        max=130000000,
    ) as bar:

        def _helper(url: str) -> None:
            authorURLs.add(repoToAuthorURLConversion(url))
            bar.next()

        for url in streamIterable:
            _helper(url)

    #        with ThreadPoolExecutor() as executor:
    #            executor.map(_helper, streamIterable)

    print("Creating a set of author URLs...")

    with open(outputFilepath, "w") as outputFile:
        outputFile.writelines(authorURLs)
        outputFile.close()


if __name__ == "__main__":
    main()
