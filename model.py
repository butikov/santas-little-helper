import re

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pickle


text_clf = Pipeline([
    ('vect', TfidfVectorizer(stop_words='english')),
    ('clf', SGDClassifier(loss='hinge', penalty='l2',
                          alpha=1e-3, random_state=42,
                          max_iter=5, tol=None)),
])


class Model:
    def __init__(self, model=None, transformer=None):
        self.transformer = transformer
        self.model = model

    def to_file(self, model_path: str, transformer_path: str):
        if self.model is not None:
            pickle.dump(self.model, open(model_path, 'wb'))
        if self.transformer is not None:
            pickle.dump(self.transformer, open(transformer_path, 'wb'))

    @classmethod
    def from_pickles(cls, model_path: str, transformer_path: str):
        return cls(pickle.load(open(model_path, 'rb')), pickle.load(open(transformer_path, 'rb')))

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        transformer = TfidfVectorizer(stop_words='english', ngram_range=(2, 3), max_df=0.9,)
        data = transformer.fit_transform(df['comment'])
        train_X, test_X, train_y, test_y = train_test_split(data, df['is_good'], test_size=0.2, random_state=42)
        model = RandomForestClassifier(max_depth=10)
        # model = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, n_jobs=-1, tol=None)
        model.fit(train_X, train_y)
        print(f1_score(test_y, model.predict(test_X)))
        return cls(model, transformer)

    def get_santa_answer(self, text: str):
        return "You are such a good! You deserve a present this year" if self.predict(text) > 0 \
            else "Unfortunately, you didn't deserve a present. Try better next year"

    def predict(self, text: str):
        words = re.findall(r"\w+", text.lower())
        if len(words) > 0:
            data = self.transformer.transform([' '.join(words)])
            return self.model.predict(data)[0]
        return -1

