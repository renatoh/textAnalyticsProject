from nltk import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class StemmedTfidfVectorizer(TfidfVectorizer):
    en_stemmer = SnowballStemmer('english')

    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (StemmedTfidfVectorizer.en_stemmer.stem(w) for w in analyzer(doc))