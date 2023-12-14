from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from collections import Counter
from sklearn.linear_model import LinearRegression


def co_occurrence(docs, window_size):
    count_model = CountVectorizer(ngram_range=(1,1), min_df=0.001) # default unigram model
    X = count_model.fit_transform(docs)
    X[X > 0] = 1
    Xc = (X.T * X)
    Xc.setdiag(0)
    X_cooc=Xc.toarray()
    indexs=np.arange(0, X_cooc.shape[0]).tolist()[:window_size] + \
    np.arange(0, X_cooc.shape[0]).tolist()[-window_size:]
    X_cooc_2=np.delete(np.delete(X_cooc, indexs, axis=0), indexs, axis=1)
    list_vocab=list(count_model.vocabulary_.keys())
    return X_cooc_2, list_vocab

######################################

def window_without_center(seq, n):
    start = 0
    seq_len = len(seq)

    while True:
        center = start + n
        end = center + n + 1

        window_index_list = range(start, end)
        yield seq[center], [seq[i] for i in window_index_list if i != center]
        
        start += 1
        if end >= seq_len:
            break
    
######################################

def get_embedding_vectors(token, word2vec:dict):
    n=50
    if token in list(word2vec.keys()):
        return word2vec[token]
    else:
        return np.zeros(n)
        
######################################

def create_context_vectors(tokens, window_size,word2vec:dict, n=50):

    target_counts=Counter()
    all_context_vecs=[]
    token_list = tokens
    for target_token, context in window_without_center(token_list, window_size):
        context_vector = np.zeros(n)
        for token in context:
            context_vector += get_embedding_vectors(token, word2vec)
            target_counts[target_token]+=1
            all_context_vecs.append(context_vector)
            
    final_dic=dict(zip(target_counts, all_context_vecs))
        
    for target_token in target_counts.keys():
        final_dic[target_token]=final_dic[target_token]/target_counts[target_token]
    return final_dic

######################################

def create_word_feature_matrix(cooc_mat, context_vec, w2v_vectors):
    return LinearRegression(fit_intercept=False).fit(np.dot(cooc_mat,context_vec), w2v_vectors).coef_.astype(np.float32)

######################################

def create_eatch_execute_embedding(tokens:list, word:str, word2vec:dict, window_size:int, transform_mat:list):
    n=50
    if (word in tokens) and (tokens.index(word)!=0) and (tokens.index(word)!=len(tokens)-1):
        center_ind = tokens.index(word)
        if ((center_ind + window_size) <= len(tokens)) and ((center_ind - window_size) >= 0):
            sub_token = tokens[(center_ind - window_size):(center_ind + window_size + 1)]
            uf = create_context_vectors(sub_token, window_size, word2vec)[word]
        else:
            uf = np.zeros(n)
    else:
        uf = np.zeros(n)
    return np.dot(transform_mat, uf)

######################################

def intersection_2lists(list1:list, list2:list):
    return [value for value in list1 if value in list2]