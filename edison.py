#!/usr/bin/env python
# coding: utf-8
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import elasticsearch

# Preparing information for connecting to Edison
CONNECTION_TIMEOUT = 120
PAGE_SIZE = 100
ES_HOST = "192.99.62.203"
ES_PORT = "9201"
ES_INDEX = "project-5bec7652be07770018d86cc4*"


class ElasticSearchHelper:
    _es_host = None
    _es_port = None
    _es_conn = None
    _use_ssl = False

    def __init__(self, es_host, es_port, use_ssl=False):
        self._es_host = es_host
        self._es_port = es_port
        self._use_ssl = use_ssl
        self.create_connection()

    # Setup connection to Edision
    def create_connection(self):
        es = elasticsearch.Elasticsearch(
            [{"host": self._es_host, "port": self._es_port}],
            timeout=CONNECTION_TIMEOUT,
            send_get_body_as="POST",
            use_ssl=self._use_ssl,
        )
        es.cluster.health()
        self._es_conn = es

    # Search function
    def search(self, index, doc_type, search, scroll=None):
        if scroll:
            return self._es_conn.search(
                index=index, doc_type=doc_type, body=search, scroll=scroll
            )
        else:
            return self._es_conn.search(index=index, doc_type=doc_type, body=search)

    def scroll(self, scroll_id, scroll="1m"):
        return self._es_conn.scroll(scroll_id=scroll_id, scroll=scroll)


# Get response from Kibana(Edison backend)
def search_kibana(res1):
    res1 = json.loads(res1)

    """Simple Elasticsearch Query"""
    query = {"size": PAGE_SIZE, "query": {"bool": {"must": res1}}}
    es_helper = ElasticSearchHelper(ES_HOST, ES_PORT)
    response = es_helper.search(ES_INDEX, None, query, "2m")
    return response


# Return the first text with highest score, if none return "I don't know"
def get_response_kibana(example_sent):
    filtered_sentence = return_filtered_sentence(example_sent)
    inner_query = get_inner_query(filtered_sentence)
    response = search_kibana(inner_query)
    if response["hits"]["total"] == 0:
        msg = "I don't know"
        return msg
    else:
        return response["hits"]["hits"][0]["_source"]["text"]


# Convert query to filtered_sentence
def return_filtered_sentence(example_sent):
    stop_words = set(stopwords.words("english"))
    stop_words.update(
        ["Where", "What", "How", "Which", "When", "'", "?", "happens", "did", "does"]
    )
    word_tokens = word_tokenize(example_sent)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence


# Creating inner query from filtered_text
def get_inner_query(filtered_sentence):
    jobj = []
    for i in range(0, len(filtered_sentence)):
        ob = {"match": {"text": filtered_sentence[i]}}
        jobj.append(ob)

    res = json.dumps(jobj)
    return res


if __name__ == "__main__":
    example_sent = "baggins"
    result = get_response_kibana(example_sent)
    print(result)
