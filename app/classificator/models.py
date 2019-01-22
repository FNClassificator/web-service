from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# -*- coding:utf-8 -*-

from app.classificator import helpers
from sklearn import svm
import pandas as pd

class Models():

    def __init__(self):
        self.cv = CountVectorizer()
        self.svm_model = None
        self.dataset = None
        self.document_fake = None 
        self.document_real = None
        return

    def create_documents(self, dataset):
        # Count vectorizer
        self.cv.fit_transform(dataset['text'].values)

        # Dataset to cv
        dataset_real = dataset.loc[dataset['label'] == 0]
        dataset_fake = dataset.loc[dataset['label'] == 1]

        cv_real = self.cv.transform(dataset_real['text'])
        cv_fake = self.cv.transform(dataset_fake['text'])

        # Create TF-IDF models
        tfidf_model_real = TfidfTransformer(use_idf=True).fit(cv_real)
        tfidf_model_fake = TfidfTransformer(use_idf=True).fit(cv_fake)

        # Get TF-IDF distribution
        tfidf_real = tfidf_model_real.transform(cv_real)
        tfidf_fake = tfidf_model_fake.transform(cv_fake)

        # Get relevant words
        topn = 600

        sorted_items= helpers.sort_coo(tfidf_real.tocoo())
        feature_names = self.cv.get_feature_names()
        results, top_real_words = helpers.extract_topn_from_vector(feature_names, sorted_items, topn)

        sorted_items= helpers.sort_coo(tfidf_fake.tocoo())
        feature_names = self.cv.get_feature_names()
        results, top_fake_words = helpers.extract_topn_from_vector(feature_names, sorted_items, topn)

        # Store documents
        self.document_real = top_real_words
        self.document_fake = top_fake_words

        self.dataset = dataset

    def compute_similarity_dataset(self):
        top_real_words_coded = self.cv.transform([' '.join(self.document_real)])
        top_fake_words_coded = self.cv.transform([' '.join(self.document_fake)])
        self.dataset['cos_fake'] = self.dataset['label']*0.000000000005
        self.dataset['cos_real'] = self.dataset['label']*0.000000000005
        for index, row in self.dataset.iterrows():
            to_number = self.cv.transform([row['text']])
            cosine_sim_fake = helpers.get_cosine_similarity(top_fake_words_coded, to_number)
            cosine_sim_real = helpers.get_cosine_similarity(top_real_words_coded, to_number)
            self.dataset.at[index,'cos_fake'] = cosine_sim_fake[0]
            self.dataset.at[index,'cos_real'] = cosine_sim_real[0]
        return self.dataset[['cos_real', 'cos_fake']].values

    def update_cv(self, content):
        self.cv = CountVectorizer()
        all_text = self.document_fake + self.document_real + content
        self.cv.fit_transform(all_text)

    def predict(self, x, y):

        dataset = pd.DataFrame()
        dataset['cos_x'] = x
        dataset['cos_y'] = y
        print(dataset)
        prediction  = self.svm_model.predict(dataset[['cos_x', 'cos_y']].values)
        return prediction

    def compute_similarity_with_document(self, content):
        self.update_cv(content)

        top_real_words_coded = self.cv.transform([' '.join(self.document_real)])
        top_fake_words_coded = self.cv.transform([' '.join(self.document_fake)]) 
        content_coded = self.cv.transform([' '.join(content)])

        similarity_real = helpers.get_cosine_similarity(top_fake_words_coded, content_coded)
        similarity_false = helpers.get_cosine_similarity(top_real_words_coded, content_coded)
        print(similarity_real,similarity_false)
        return similarity_real, similarity_false

    def train_SVM_model(self):
        # Compute similarity
        X_input = self.compute_similarity_dataset()
        Y_input = self.dataset['label'].values

        # Create model
        rbf_values = helpers.svc_param_selection(X_input, Y_input, 2, 'rbf')
        self.svm_model = svm.SVC(kernel='rbf', C= rbf_values['C'], gamma=rbf_values['gamma'])
        # Train model
        self.svm_model.fit(X_input, Y_input)
        print(self.svm_model.predict(X_input))

