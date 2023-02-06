import argparse
from argparse import ArgumentParser, Namespace
from hashlib import md5
from json import dump, load
from os import makedirs, remove
from pathlib import PurePath


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="PRIME LSS File Rehasher",
        usage="A bodge to fix files whose filenames are derived from Python's hash() function",
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Filepath to inline fix",
        nargs=argparse.REMAINDER,
    )
    return parser.parse_args()


def main() -> None:
    args: Namespace = getArgs()

    makedirs(name="md5", exist_ok=True)

    oldFilePath: PurePath = PurePath(args.input[0])

    with open(oldFilePath, "r") as jsonFile:
        data: dict = load(fp=jsonFile)
        jsonFile.close()

    url: str = data["OriginalURL"]
    urlBytes: bytes = url.encode("UTF-8")
    urlMD5: str = md5(string=urlBytes).hexdigest()
    newFilePath: PurePath = PurePath(f"md5/{urlMD5}.json")
    data["id"] = urlMD5

    with open(newFilePath, "w") as jsonFile:
        dump(obj=data, fp=jsonFile, indent=4)
        jsonFile.close()

    remove(oldFilePath)


if __name__ == "__main__":
    main()
