# implement CIKM’15, Short Text Similarity with Word Embeddings
# link: https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/kenter-short-2015.pdf
import pickle
import gensim

def deep_bm25(word, query, idf, model, avg_len):
    b = 0.75
    k = 1.2
    sim_list = []

    for w in query:
        if word in model and w in model:
            sim_list.append(model.similarity(word, w))

    if len(sim_list) == 0:
        return 0
    max_sim = max(sim_list)

    return idf[word] * ((max_sim * (k + 1)) / (max_sim + k * (1 - b + (b * len(query) / avg_len))))

if __name__ == '__main__':
    base = './data/'
    train_path = base + 'train.pickle'
    test_path = base + 'test.pickle'
    avg_len = 11.264802991615534

    idf_path = base + 'idf.pickle'
    glove_path = '/tmp2/bschang/glove-word2vec.txt'
    fasttext_path = '/tmp2/bschang/fasttext-word2vec.txt'

    output_path = base + 'train_bm25_other.pickle'
    # output_path = base + 'test_bm25_other.pickle'

    with open(train_path, 'rb') as f:
        train = pickle.load(f)
    with open(test_path, 'rb') as f:
        test = pickle.load(f)
    with open(idf_path, 'rb') as f:
        idf = pickle.load(f)

    glove_model = gensim.models.KeyedVectors.load_word2vec_format(glove_path, binary=False)
    fasttext_model = gensim.models.KeyedVectors.load_word2vec_format(fasttext_path, binary=False)

    result = []
    if 'train' in output_path:
        for i, instance in enumerate(train):
            len_q1 = len(instance['question1'])
            len_q2 = len(instance['question2'])
            if len_q1 > len_q2:
                q1 = instance['question1']
                q2 = instance['question2']
            else:
                q1 = instance['question2']
                q2 = instance['question1']
            glove_score = 0.0
            fasttext_score = 0.0

            for word in q1:
                glove_score += deep_bm25(word, q2, idf, glove_model, avg_len)
                fasttext_score += deep_bm25(word, q2, idf, fasttext_model, avg_len)
            result.append([glove_score, fasttext_score])
    else:
        for i, instance in enumerate(test):
            len_q1 = len(instance['question1'])
            len_q2 = len(instance['question2'])
            if len_q1 > len_q2:
                q1 = instance['question1']
                q2 = instance['question2']
            else:   
                q1 = instance['question2']
                q2 = instance['question1']
            glove_score = 0.0
            fasttext_score = 0.0

            for word in q1:
                glove_score += deep_bm25(word, q2, idf, glove_model, avg_len)
                fasttext_score += deep_bm25(word, q2, idf, fasttext_model, avg_len)
            result.append([glove_score, fasttext_score])

    with open(output_path, 'wb') as f:
        pickle.dump(result, f)
