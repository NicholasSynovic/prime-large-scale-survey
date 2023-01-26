import requests
from requests import Response

url = ['https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods', 
    'https://www.oreilly.com/library/view/python-in-a/0596001886/ch04s09.html', 
    'https://www.google.com/docs/abou'] #Last Url should give you a 404 error

r: Response = requests.get(url)
print(f"""
DATE = {r.headers['Date']}  
Content-Type = {r.headers['Content-Type']}
""")

print(f"Status Code: {r.status_code}\n") 

#Working on for loop to use with if statements
#Take from list of urls
#for url:

if r.status_code == 200: 
    print("The URL is OK")
elif r.status_code == 404:
    print("The URL is not found")
elif r.status_code == 502:
    print("Bad Gateway")

