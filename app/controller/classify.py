

from app.scrapping import scrapping as s
from app.translator import translator as t
from app.preprocessor import clean_text as ct

def classify_article(url, page):
    # 1 Scrap
    web_content = s.get_url_content(url, page)

    # 2 Traducir
    web_en_content = t.translate_document(web_content)

    # 3 Preprocesar
    document = ct.tokenize_document(web_en_content)

    # 4 Codificar

    # 5 Validar
    return