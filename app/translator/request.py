
from app import *
import requests
import json

headers = {
    "Ocp-Apim-Subscription-Key": MICROSOFT_KEY,
    "Content-Type": "application/json"
}


def make_request(list_texts):
    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=es&to=en'
    
    payload = [ ]
    for text in list_texts:
        aux = {
            'Text': text
        }
        payload.append(aux)

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())
    return r.json()