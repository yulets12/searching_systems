import pandas as pd
import xml.etree.ElementTree as ET
import base64
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import re
from fuzzywuzzy import process, fuzz
import numpy as np


LEN_SHINGLE = 5
MATCH_THRESHOLD = 70
CLUSTER_THRESHOLD = 0.2

'''
patterns = "[0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stop_words = stopwords.words('russian')
morph = MorphAnalyzer()
def data_preprocessing(data): # подготовка текстов
    data = re.sub(patterns, ' ', data) # удаляем все не буквы
    tokens = []
    for token in data.split():
        if token and token.lower() not in stop_words:  # выбрасываем стоп-слова
            token = token.strip()
            token = morph.normal_forms(token)[0]  # лемматизация
            tokens.append(token)
    return ' '.join(tokens).strip()

xml_data = open('news-shevard.xml', 'r')

root = ET.parse(xml_data).getroot() # xml дерево

data = []
columns = []
for i in range(len(list(root))):     # выделяем все листья дерево (тип + содержимое)
    node = list(root)[i]
    data.append([subnode.text for subnode in list(node)])
    columns = [subnode.tag for subnode in list(node)]

doc_df = pd.DataFrame(data)  # сохраняем данные в датафрейм
doc_df.columns = columns
xml_data.close()
doc_df['content'] = doc_df['content'].apply(lambda x: data_preprocessing(base64.b64decode(x).decode('windows-1251')))  # декодирование и лемматизация документов
doc_df.to_csv('prepared.csv', columns = ['docID', 'content'])  # сохраняем очищенные данные в файл

#Продолжаем с очищенными данными
data = np.genfromtxt('prepared.csv', delimiter=',', encoding='utf8', dtype=None)      #тут фильтровали очищенные данные, чтобы было хоть что-то похожее
data = data[1:]
data = np.transpose(data)
np.savetxt("sorted.csv", data[data[:, 2].argsort()], delimiter=",")
'''

def find_shingles(text):   # бьем все тексты на шинглы
    items = text.split()
    shingles = []
    for i in range(len(items) - LEN_SHINGLE + 1):
        shingle = items[i:i+LEN_SHINGLE]
        shingles.append(' '.join(shingle))
    return shingles

def compare_shingles(sh1, sh2):  # сравниваем шинглы двух текстов
    matches_cnt = 0
    for shingle in sh1:
        match = process.extractOne(shingle, sh2)
        if match[1] > MATCH_THRESHOLD:
            matches_cnt += 1

    return matches_cnt / ((len(sh1) + len(sh2))/2)



#Работаем с отфильтрованными данными
data = np.genfromtxt('filtered.csv', delimiter=',', encoding='utf8', dtype=None)
n = len(data)

shingles = []
for i in range(n):
    shingles.append(find_shingles(data[i]))

matches = []
clusters = []

for i in range(n):
    print(f'Text {i}:')
    matches.append([])
    for j in range(n):
        if i != j:
            metric = compare_shingles(shingles[i], shingles[j])
            print(f'--- text {j}: threshold = {metric}, match = ', metric > CLUSTER_THRESHOLD)
            if metric > CLUSTER_THRESHOLD:
                matches[i].append(j)
                flag = False
                for cluster in clusters:
                    if i in cluster or j in cluster:
                        cluster.add(i)
                        cluster.add(j)
                        flag = True
                if not flag:
                    clusters.append({i, j})
    print('\n----------------------------------------------------------\n')

print('Clusters: ', clusters)












