from elasticsearch import Elasticsearch


class Query:
    def __init__(self, host, port, index_name='habr-index'):
        hosts = [{"host": host, "port": port}]
        self.es = Elasticsearch(hosts)
        assert self.es.ping(), f"Query.__init__: Can not connect to {host}:{port}"

        self.index_name = 'habrhabr_posts'

    @staticmethod
    def parse_out(res):
        hits = res['hits']['hits']
        out = [{name: r['_source'][name] for name in r['_source']} for r in hits]
        return out

    # Получает список тем публикации
    @staticmethod
    def parse_hubs(raw_hubs):
        hub_list = [hub_str.strip().lower() for hub_str in raw_hubs.strip().replace(', ', '').split('\n')]
        return [hub for hub in hub_list if hub]

    # Возвращает тексты, соответствующие заголовку
    # query - текст запроса
    # tag - тег, по которому осуществляется поиск
    # flag:
    #   -1 - искать полное совпадение,
    #   0 - искать полное вхождение в текст,
    #   >0 искать вхождение в текст с возмодностью slop пропусков между словами
    def get_by_tag_content(self, tag, query, relevant_hubs=None, slop=0, size=9000):
        if relevant_hubs:
            hubs_query = {'query': {'bool': {'should': [
			{'match_phrase': {"hubs": {'query': hub, 'operator': 'and'}}} for hub in relevant_hubs]}}}
        else:
	        hubs_query = None

        if slop < 0:
            query_object = {'match': {tag: {'query': query, 'operator': 'and'}}}
        elif slop == 0:
            query_object = {'match_phrase': {tag: query}}
        else:
            query_object = {'match_phrase': {tag: {'query': query, 'slop': slop}}}

        if hubs_query:
            query_object = {'query': {'bool': {'must': [query_object, hubs_query]}}}
        else:
            query_object = {'query': query_object}

        query_object["size"] = size
        res = self.es.search(index=self.index_name, body=query_object)
        return self.parse_out(res)

    def get_by_title(self, query, relevant_hubs=None, slop=-1):
        res = self.get_by_tag_content('title', query, relevant_hubs, slop)
        assert not relevant_hubs or len(set(relevant_hubs).intersection(set(self.parse_hubs(query['hubs'])))) != 0
        return res

    def get_by_text(self, query, relevant_hubs=None, slop=-1):
        res = self.get_by_tag_content('text', query, relevant_hubs, slop)
        assert not relevant_hubs or len(set(relevant_hubs).intersection(set(self.parse_hubs(query['hubs'])))) != 0
        return res

    def get_by_hub(self, query):
        res = self.get_by_tag_content('hubs', query, slop=0)
        # Перестраховка
        return [text for text in res if query in self.parse_hubs(query['hubs'])]
        
    def get_by_id(self, doc_id):
        res = self.get_by_tag_content('doc_id', doc_id, slop=0)
        assert len(res) == 1
        return res[0]

