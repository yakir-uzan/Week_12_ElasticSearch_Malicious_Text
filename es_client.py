from elasticsearch import Elasticsearch

def es():
    es_client = Elasticsearch("http://localhost:9200", request_timeout=60, retry_on_timeout=True, max_retries=3)
    info = es_client.info()
    print(info.get('cluster_name'))
    print(info.get('version'))
    return es_client

