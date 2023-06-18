import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

def data_preprocessing(data): #Токенизация, лемматизация, удаление стоп слов
    res = []
    stop_words = stopwords.words('russian')
    lemmatizer = WordNetLemmatizer()
    for item in data:
        item = word_tokenize(item)
        item = [w for w in item if w not in stop_words]
        item = [lemmatizer.lemmatize(w) for w in item]
        res.append(' '.join(item))
    return res

def print_info(real, predicted):   # Оцениваем результат
    print("Матрица ошибок:")
    matrix = confusion_matrix(real, predicted)
    print(matrix)
    acc = accuracy_score(real, predicted)
    prec, rec, fscore, support = precision_recall_fscore_support(real, predicted, average='macro')
    print("Accuracy:", acc) # доля правильных ответов
    print("Precision:", prec) # точность, tp/tp+fp
    print("Recall:", rec) # полнота, tp/tp+fn
    print("F-measure:", fscore)

#Базовая подготовка данных
df = pd.read_csv('labeled.csv')

symbols = ['.', ',', '/', '\\', '\\n', '"', ';', ':', ')', '(', '&', '!', '?', '-', '#', '@', "'", '<', '>']
comments = []
toxic = []
for j in range (len(df)):
    toxic.append(df['toxic'][j])
    comments.append(df['comment'][j])
    for symb in symbols:
        comments[j] = comments[j].replace(symb, ' ')
    for symb in [' '*x for x in range(2, 11)]:
        comments[j] = comments[j].replace(symb, ' ')
    comments[j] = comments[j].strip().lower()

new_df = pd.DataFrame({'comment': comments, 'toxic': toxic})
new_df.to_csv('labeled_prep.csv', index=False)

#Продолжаем с очищенными данными
data = np.genfromtxt('labeled_prep.csv', delimiter=',', encoding='utf8', dtype=None)
data = data[1:]
data = np.transpose(data)

[comment], [toxic] = np.split(data, 2)
comment = data_preprocessing(comment)

# Векторизация
tvectorizer = TfidfVectorizer()
comment = tvectorizer.fit_transform(comment)

# Делим на тест и треин
X_train, X_test, y_train, y_test = train_test_split(comment, toxic, test_size=0.33, random_state=0)
# Классифицируем
knc = KNeighborsClassifier()
knc.fit(X_train, y_train)
res = knc.predict(X_test)

print("Анализ результатов:")
print_info(y_test, res)
