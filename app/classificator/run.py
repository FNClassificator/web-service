
from app.classificator.models import Models

import pandas as pd
from app.utils import io



def create_classifier():
    # Import file
    articles = io.read_json_file('app/data/dataset_content.json')
    df = pd.DataFrame(data=articles['articles']) # Put in pandas dataframe

    # Create dataset
    dataset = pd.DataFrame()
    dataset['text'] = join_lists(df, ['all_word'])
    dataset['label'] = df['fake']*1

    models = Models()
    models.create_documents(dataset)
    models.train_SVM_model()
    return models


def predict_document(models, content):
    sim_real, sim_fake = models.compute_similarity_with_document(content)
    prediction = models.predict(sim_real,sim_fake)
    print(prediction)
    return prediction

def join_lists(dataset, word_lists):
    result = []
    for _, row in dataset.iterrows():
        text_join = ""
        for feature in word_lists:
            doc_list = row[feature]
            text_join += ' '.join(doc_list)
        result.append(text_join)
    return result