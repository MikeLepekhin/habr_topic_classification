import os
import pickle
from heapq import nlargest

'''
Хабр - это такой идеальный ресурс, который не требует ни дедубликации, ни очистики текста от подписей к картинкам (их нет), ни другой возни. 
'''

# Получает список тем публикации
def parse_hubs(raw_hubs):
    hub_list = [hub_str.strip().lower() for hub_str in raw_hubs.strip().replace(', ', '').split('\n')]
    return [hub for hub in hub_list if hub]


# Считает частоты тем в корпусе
def count_hubs(texts):
    hubs_counter = {}
    for text in texts:
        for hub in parse_hubs(text['hubs']):
            if hub in hubs_counter:
                hubs_counter[hub] += 1
            else:
                hubs_counter[hub] = 1
    return hubs_counter


# Находит n самых частых тем
def find_n_max_hubs(texts, n):
    hubs_counter = count_hubs(texts)
    return nlargest(n, hubs_counter, key = hubs_counter.get)


# Фильтрует тексты, выбирая только принадлежащие к n самым частым темам
def filter_texts_by_habs(texts, n):
    result = []
    hubs = find_n_max_hubs(texts, n)
    for text in texts:
        if bool(set(hubs) & set(parse_hubs(text['hubs']))):
            result.append(text['id'])
    return result


# Возвращает список id текстов, прошедших фильтрацию
def filter(dir, n):
    texts = []

    for filename in os.listdir(dir):
        text = pickle.load(open(os.path.join(dir, filename), 'rb'))
        texts.append(text)

    return filter_texts_by_habs(texts, 10)


if __name__ == "__main__":
    filtered = filter('clean_files', 10)
