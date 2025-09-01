from elasticsearch import Elasticsearch

class ElasticConnector:
    """ create connection to elastic """
    def __init__(self):
        self.client = Elasticsearch("http://localhost:9200", request_timeout = 60, retry_on_timeout = True, max_retries = 3)
        self.get_info()

    """ print cluster & version """
    def get_info(self):
        info = self.client.info()
        return f"info of connection: \n{info}"

    def get_client(self):
        return self.client
