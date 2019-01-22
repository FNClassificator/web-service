

from app.scrapping import scrapping as s
from app.translator import translator as t
from app.preprocessor import clean_text as ct
from app.classificator import run as r

def classify_article(url, page, models):
    # 1 Scrap
    web_content = s.get_url_content(url, page)

    # 2 Traducir
    #web_en_content = t.translate_document(web_content)

    # 3 Preprocesar
    document = ct.tokenize_document(web_content)
    print(document)
    # 4 Predecir
    prediction = r.predict_document(models, document)
    return prediction[0]