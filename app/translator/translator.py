
import os
from app.utils import io
from app.utils import translate


def translate_document(content):

    title, subtitle = request_title_subtitle(content)
    text_body = request_body(content)

    content['title'] = title
    content['subtitle'] = subtitle
    content['text'] = text

    return content

def request_title_subtitle(content):
    if content['title'] == content['subtitle']:
        resp = translate.make_request([content['title']])
        title = resp[0]['translations'][0]['text']
        subtitle = title
    elif content['subtitle'] == '':
        resp = translate.make_request([content['title']])
        title = resp[0]['translations'][0]['text']
        subtitle = ''
    else:
        resp = translate.make_request([content['title'], content['subtitle']])
        title = resp[0]['translations'][0]['text']
        subtitle = resp[1]['translations'][0]['text']
    return title, subtitle

def request_body(content):
    rest_two = translate.make_request(content['text'])
    text_body = []
    # TODO: Check if too much text
    for elem in rest_two:
        text_body.append(elem['translations'][0]['text'])
    return text_body