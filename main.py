import jieba
import os
import math
import pandas as pd

# 目录文件遍历器
def path_iterator(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                yield os.path.join(root, file)

# 读取停用词表
def get_stopwords():
    stopwords = set()
    for filepath in path_iterator('./stopwords'):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stopwords.add(line.strip())
    return stopwords

# 计算TF-IDF
def calc_tfidf(stopwords):
    tf = dict()
    idf = dict()
    tf_idf = dict()
    for filepath in path_iterator('./data'):
        tf_j = dict()
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        words = jieba.lcut(content)
        for word in words:
            if word in stopwords or len(word) == 1:  # 跳过停用词、单字词
                continue
            if word in tf_j:
                tf_j[word] += 1
            else:
                tf_j[word] = 1
        for word, _ in tf_j.items():
            if word in idf:
                idf[word] += 1
            else:
                idf[word] = 1
        tf[filepath] = tf_j
    docNum = len(tf)
    for filepath, tf_j in tf.items():
        tf_idf_j = dict()
        wordNum = sum(tf_j.values())
        for word, count in tf_j.items():
            tf_idf_j[word] = count / wordNum * math.log(docNum / idf[word])
        tf_idf[filepath] = tf_idf_j
    return tf_idf


stopwords = get_stopwords()
result = calc_tfidf(stopwords)
for filepath, tf_idf in result.items():
    wordList = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(wordList, columns=['词', 'TFIDF'])
    df.to_csv(filepath.replace('.txt', '.csv'))
