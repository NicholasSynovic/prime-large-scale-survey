import subprocess
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5
from io import TextIOWrapper
from json import dump
from os import makedirs
from os.path import isfile
from pathlib import PurePath
from subprocess import CompletedProcess
from time import sleep, time
from typing import List
from urllib.parse import ParseResult, urlparse

import requests
from requests import Response

from prime_lss.primeLSS import PrimeLSSElement

sleepSecond: int = 60


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
        "-d",
        "--directory",
        required=True,
        help="Directory to store output .json file",
    )
    return parser.parse_args()


def getURL(url: str) -> Response:
    headers: dict = {"User-Agent": "PRIME Large Scale Survey"}
    while True:
        resp: Response = requests.get(url=url, allow_redirects=False, headers=headers)

        if resp.status_code == 200 or 301 or 404:
            break
        else:
            sleep(secs=sleepSecond)
            sleepSecond = sleepSecond**2

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
    elementID: str = md5(originalURL.encode("UTF-8")).hexdigest()
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


# def concurrentResolve(streamIter: map, rootDir: PurePath) -> None:
#     def _helper(url: str) -> None:
#         print(f"Resolving {url} ...")
#         resp: Response = getURL(url)
#         p: PrimeLSSElement = buildElement(resp)
#         # jsonObjects.append(p.to_dict())
#         out: PurePath = PurePath(f"{rootDir}/{p.id}.json")
#         writeToFile(outputFilePath=out, data=p.to_dict())

#     with ThreadPoolExecutor() as executor:
#         executor.map(_helper, streamIter)


def writeToFile(outputFilePath: PurePath, data: dict) -> None:
    with open(file=outputFilePath, mode="w") as json:
        dump(obj=data, fp=json, indent=4)
        json.close()


def main() -> None:
    args: Namespace = parseArgs()

    inputFilePath: PurePath = PurePath(args.input)
    outputDirectory: PurePath = PurePath(args.directory)

    stream: TextIOWrapper = open(file=inputFilePath, mode="r", buffering=1)
    streamIterable: map = map(str.strip, iter(stream.readline, ""))

    # concurrentResolve(streamIter=streamIterable, rootDir=outputFilePath)

    url: str
    for url in streamIterable:
        testFileName: PurePath = PurePath(
            f"{outputDirectory}/{url.encode('UTF-8').hexdigest()}.json"
        )

        if f'{md5(url.encode("UTF-8")).hexdigest()}.json' == testFileName:
            continue

        print(f"Resolving {url} ...")
        resp: Response = getURL(url)
        p: PrimeLSSElement = buildElement(resp)
        pDict: dict = p.to_dict()
        outputFilePath: PurePath = PurePath(f"{outputDirectory}/{pDict['id']}.json")
        writeToFile(outputFilePath, data=pDict)


if __name__ == "__main__":
    main()
