
import os
from app.utils import io
from app.translator import request


def translate_document(content):

    title, subtitle = request_title_subtitle(content)

    text_body = request_body(content)

    content['title'] = title
    content['subtitle'] = subtitle
    content['text'] = text_body

    return content

def request_title_subtitle(content):
    if content['title'] == content['subtitle']:
        resp = request.make_request([content['title']])
        title = resp[0]['translations'][0]['text']
        subtitle = title
    elif content['subtitle'] == '':
        resp = request.make_request([content['title']])
        title = resp[0]['translations'][0]['text']
        subtitle = ''
    else:
        resp = request.make_request([content['title'], content['subtitle']])
        title = resp[0]['translations'][0]['text']
        subtitle = resp[1]['translations'][0]['text']
    return title, subtitle


def req_sub_text(content):
    rest_two = request.make_request(content)
    text_body = []
    # TODO: Check if too much text
    for elem in rest_two:
        text_body.append(elem['translations'][0]['text'])
    return text_body
    

def get_size(list_of_text):
    size = 0
    for element in list_of_text:
        size += len(element)
    return size

def request_body(content):

    text_size = get_size(content['text'])

    if text_size > 500:
        split_n = len(content['text']) // 2
        text_one = content['text'][:split_n]
        text_body_one = req_sub_text(text_one)
        text_two = content['text'][split_n:]
        text_body_two = req_sub_text(text_two)
        return text_body_one + text_body_two

    else: 
        text_body = req_sub_text(content['text'])
        return text_body