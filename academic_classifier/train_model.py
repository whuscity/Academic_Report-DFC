
import re
import string
import jieba
from sklearn import metrics
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from connectdb import prepare_datasets
import pickle
from sklearn.feature_extraction.text import CountVectorizer
'''数据预处理'''

def tokenize_text(text):
    tokens = jieba.cut(text)
    tokens = [token.strip() for token in tokens]
    return tokens


def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def remove_stopwords(text):
    tokens = tokenize_text(text)# 加载停用词
    with open("hlt_stop_words.txt", encoding="utf8") as f:
        stopword_list = f.readlines()
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    filtered_text = ''.join(filtered_tokens)
    return filtered_text


def normalize_corpus(corpus, tokenize=False):
    normalized_corpus = []
    for text in corpus:
        text = remove_special_characters(text)
        text = remove_stopwords(text)
        normalized_corpus.append(text)
        if tokenize:
            text = tokenize_text(text)
            normalized_corpus.append(text)

    return normalized_corpus

'''特征提取'''


from sklearn.feature_extraction.text import TfidfTransformer

def tfidf_transformer(bow_matrix):
    transformer = TfidfTransformer(norm='l2',
                                   smooth_idf=True,
                                   use_idf=True)
    tfidf_matrix = transformer.fit_transform(bow_matrix)
    return transformer, tfidf_matrix

from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_extractor(corpus, ngram_range=(1, 1)):
    vectorizer = TfidfVectorizer(min_df=1,
                                 norm='l2',
                                 smooth_idf=True,
                                 use_idf=True,
                                 ngram_range=(1, 1))
    features = vectorizer.fit_transform(corpus)
    return vectorizer, features

def get_metrics(true_labels, predicted_labels):
    print('Accuracy:', np.round(
        metrics.accuracy_score(true_labels,
                               predicted_labels),2))
    print('Precision:', np.round(
        metrics.precision_score(true_labels,
                                predicted_labels,
                                average='weighted'),2))
    print('Recall:', np.round(
        metrics.recall_score(true_labels,
                             predicted_labels,
                             average='weighted'),  2))
    print('F1 Score:', np.round(
        metrics.f1_score(true_labels,
                         predicted_labels,
                         average='weighted'), 2))


def train_predict_evaluate_model(classifier,
                                 train_features, train_labels,
                                 test_features, test_labels):
    # build model
    clf = classifier.fit(train_features, train_labels)
    predictions = classifier.predict(test_features)
    # evaluate model prediction performance
    get_metrics(true_labels=test_labels,
                predicted_labels=predictions)
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f, pickle.HIGHEST_PROTOCOL)
    return predictions


if __name__ == '__main__':
    train_X,train_Y,test_X,test_Y = prepare_datasets()
    normalize_corpus_train_x = normalize_corpus(train_X)
    normalize_corpus_test_x = normalize_corpus(test_X)
    mnb = MultinomialNB()
    svm = SGDClassifier(loss='hinge')
    lr = LogisticRegression()
    vector = CountVectorizer(min_df=1, ngram_range=(1,1))
    
    # print(vector.vocabulary)#
    bow_train_features = vector.fit_transform(normalize_corpus_train_x)
    bow_test_features = vector.transform(normalize_corpus_test_x)
    # 基于词袋模型的多项朴素贝叶斯
    print("基于词袋模型特征的贝叶斯分类器")
    mnb_bow_predictions = train_predict_evaluate_model(classifier=mnb,
                                                       train_features=bow_train_features,
                                                       train_labels=train_Y,
                                                       test_features=bow_test_features,
                                                       test_labels=test_Y)
    # 基于词袋模型特征的逻辑回归
    print("基于词袋模型特征的逻辑回归")
    lr_bow_predictions = train_predict_evaluate_model(classifier=lr,
                                                      train_features=bow_train_features,
                                                      train_labels=train_Y,
                                                      test_features=bow_test_features,
                                                      test_labels=test_Y)
    with open('vect.pkl', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(vector, f, pickle.HIGHEST_PROTOCOL)
    #
    # 基于词袋模型的支持向量机方法
    print("基于词袋模型的支持向量机")
    svm_bow_predictions = train_predict_evaluate_model(classifier=svm,
                                                       train_features=bow_train_features,
                                                       train_labels=train_Y,
                                                       test_features=bow_test_features,
                                                       test_labels=test_Y)

    vectorizer = TfidfVectorizer(min_df=1, norm='l2',smooth_idf=True,use_idf=True,ngram_range=(1, 1))
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f, pickle.HIGHEST_PROTOCOL)
    tfidf_train_features = vectorizer.fit_transform(normalize_corpus_train_x)
    tfidf_test_features = vectorizer.transform(normalize_corpus_test_x)
    # 基于tfidf的多项式朴素贝叶斯模型
    print("基于tfidf的贝叶斯模型")
    mnb_tfidf_predictions = train_predict_evaluate_model(classifier=mnb,
                                                         train_features=tfidf_train_features,
                                                         train_labels=train_Y,
                                                         test_features=tfidf_test_features,
                                                         test_labels=test_Y)
    # 基于tfidf的逻辑回归模型
    print("基于tfidf的逻辑回归模型")
    lr_tfidf_predictions = train_predict_evaluate_model(classifier=lr,
                                                        train_features=tfidf_train_features,
                                                        train_labels=train_Y,
                                                        test_features=tfidf_test_features,
                                                        test_labels=test_Y)

    # 基于tfidf的支持向量机模型
    print("基于tfidf的支持向量机模型")
    svm_tfidf_predictions = train_predict_evaluate_model(classifier=svm,
                                                         train_features=tfidf_train_features,
                                                         train_labels=train_Y,
                                                         test_features=tfidf_test_features,
                                                         test_labels=test_Y)
    #
