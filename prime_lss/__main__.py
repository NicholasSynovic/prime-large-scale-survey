import subprocess
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from io import TextIOWrapper
from json import dump
from pathlib import PurePath
from subprocess import CompletedProcess
from time import sleep, time
from typing import List
from urllib.parse import ParseResult, urlparse

import requests
from primeLSS import PrimeLSSElement
from requests import Response

jsonObjects: List[dict] = []


def parseArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="PRIME Large Scale Survey URL Resolver",
        usage="A tool to resolve GitHub URLs prior to cloning repositories",
        epilog="This software is dependent upon git being installed",
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input .txt file containing URLs to resolve",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output .json file for where to store data",
    )
    return parser.parse_args()


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

    commandOutput: CompletedProcess[bytes] = subprocess.run(
        args=command, shell=False, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )

    return commandOutput.returncode


def buildElement(resp: Response) -> PrimeLSSElement:
    action: int
    gitPingStatus: int

    originalURL: str = resp.url
    elementID: int = hash(originalURL)
    originalStatusCode: int = resp.status_code
    newURL: str | None = resp.headers.get("Location")

    if newURL == None:
        newURL = originalURL

    match originalStatusCode:
        case 200:
            action = 0
            gitPingStatus = gitPing(url=newURL)
        case 404:
            action = -1
            gitPingStatus = -1
        case 301:
            action = 1
            gitPingStatus = gitPing(url=newURL)
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


def concurrentResolve(streamIter: map) -> None:
    def _helper(url: str) -> None:
        print(f"Resolving {url}...")
        resp: Response = getURL(url)
        p: PrimeLSSElement = buildElement(resp)
        jsonObjects.append(p.to_dict())

    with ThreadPoolExecutor() as executor:
        executor.map(_helper, streamIter)


def main() -> None:
    args: Namespace = parseArgs()

    inputFilePath: PurePath = PurePath(args.input)
    outputFilePath: PurePath = PurePath(args.output)

    stream: TextIOWrapper = open(file=inputFilePath, mode="r", buffering=1)
    streamIterable: map = map(str.strip, iter(stream.readline, ""))

    start: int = time()

    concurrentResolve(streamIter=streamIterable)

    # url: str
    # for url in streamIterable:
    #     print(f"Resolving {url}...")
    #     resp: Response = getURL(url)
    #     p: PrimeLSSElement = buildElement(resp)
    #     jsonObjects.append(p.to_dict())

    end: int = time()

    print(f"Saving file to {outputFilePath}...")
    with open(file=outputFilePath, mode="w") as json:
        dump(obj=jsonObjects, fp=json, indent=4)
        json.close()

    print(f"{end - start} seconds")


if __name__ == "__main__":
    main()
