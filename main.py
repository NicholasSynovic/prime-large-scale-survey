import requests
from requests import Response
from itertools import islice
from io import TextIOWrapper
import concurrent.futures

from primeLSS import PrimeLSSElement
from time import sleep

# def url_stream():
#     index = 0
#     with open('mergedurls.txt','r') as file:
#         while True:
#             lines = list(islice(file, 1000))
#             for line in lines:
#                 index += 1
#                 #print(line)
#                 print(f"Total count is {index}")    
#             if not lines:
#                 break


# def get_url():
#         r = requests.get(url_stream())
#         print(r)

# url_stream()




# def main()  ->  None:
#     stream: TextIOWrapper = open(file="url.txt", mode="r", buffering=1)

#     streamIterable = iter(stream.readline, '')

#     line: str
#     for line in streamIterable:
#         return(line.strip())

# if __name__ == "__main__":
#     main()

# def main() -> None:
#     with open("largeurls.txt", "r") as stream:
#         lines = stream.readlines()

    
#     for line in lines:
#         url = line.strip()
#         r = requests.get(url)
#         print(r, url)

# if __name__ == "__main__":
#     main()


jsonObjects: list[dict] = []

def fetch_url(url: str) -> None:
    r: Response = requests.get(url, allow_redirects=False)

    if r.status_code == 429:
        sleep(secs=60)
        fetch_url(url)
        return None

    newURL: str | None = r.headers.get("Location")

    if newURL == None:
        newURL = url
    

    p: PrimeLSSElement = PrimeLSSElement(id=hash(url), original_url=url, new_url=newURL, original_url_status_code=str(r.status_code), action=0)

    jsonObjects.append(p.to_dict())

    #print(r.status_code)
    print(p.to_dict())

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

