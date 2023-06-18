import  pandas as pd
from nltk import sent_tokenize
from rusenttokenize import ru_sent_tokenize
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from pymystem3 import Mystem
from sklearn.feature_extraction.text import TfidfVectorizer



df = pd.read_csv('labeled_prep.csv')
print(df.head())
stemmer = SnowballStemmer('russian')
stop_words = stopwords.words('russian')
mystem = Mystem()
print(stop_words)
tvectorizer = TfidfVectorizer()

comments = []
toxic =[]
for i in range(len(df)):
    text = df['comment'][i]
    print(text)
    tokenized_text = list(ru_sent_tokenize(text)[0].split(' '))
    print("tok", tokenized_text)
    tokenized_text = [w for w in tokenized_text if w not in stop_words]
    print("stop", tokenized_text)
    stemmed_text = [stemmer.stem(word) for word in tokenized_text[:30]]
    print("stem", stemmed_text)
    lem_text = [mystem.lemmatize(w)[:10][0] for w in stemmed_text]
    print("lem", lem_text)
    string = ''
    for
    print([' '.join(w) for w in lem_text])
    comments.append([' '.join(w) for w in lem_text][0].lstrip(" "))
    print(comments)
    break





##ru_sent_tokenize(text)[:10]

##

