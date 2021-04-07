import math
import nltk
import pickle
import string

from collections import Counter
from nltk.corpus import stopwords
from os import listdir
from tqdm import tqdm

def is_correct_word(word):
    return all('а' <= ch <= 'я' for ch in word)

def calc_pmi_bigrams(text_list, remove_stopwords=True):
    punct_remover = str.maketrans('', '', string.punctuation)
    ru_stopwords = set(stopwords.words("russian"))

    total_words_num = 0
    total_bigrams_num = 0

    words_num = Counter()
    bigrams_num = Counter()

    for text in tqdm(text_list):
        word_list = text.translate(punct_remover).lower().split()
        word_list = [word for word in word_list if is_correct_word(word) and (not remove_stopwords or word not in ru_stopwords)]
        total_words_num += len(word_list)
        total_bigrams_num += len(word_list) - 1
        
        for word in word_list:
            words_num[word] += 1
        for word_id in range(1, len(word_list)):
            bigrams_num[(word_list[word_id-1], word_list[word_id])] += 1

    pmi_list = []

    for bigram, cur_bigram_num in bigrams_num.items():
        prob_bigram = cur_bigram_num / total_bigrams_num
        prob_word1 = words_num[bigram[0]] / total_words_num
        prob_word2 = words_num[bigram[1]] / total_words_num
        cur_pmi = math.log(prob_bigram) / math.log(prob_word1) / math.log(prob_word2)
        pmi_list.append((bigram, cur_pmi))
    return sorted(pmi_list, key=lambda x: -x[1])

def print_top_bigrams(text_list, k=100):
    for bigram, pmi in calc_pmi_bigrams(text_list)[:k]:
        print(bigram, pmi)

if __name__ == '__main__':
    nltk.download('stopwords')
    text_list = [pickle.load(open(f'clean_files/{filename}', 'rb'))['text']\
                 for filename in listdir('clean_files')]
    print_top_bigrams(text_list)

