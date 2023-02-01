#import requests
#from requests import Response
from itertools import islice

#index = 0
with open('mergedurls.txt','r') as file:
    while True:
        lines = list(islice(file, 1000))
        for line in lines:
            #index += 1
            print(line)
        if not lines:
            break




