from app.client import ElasticConnector
from app.mapping import TextMapping

class Indexer:
    def __init__(self, index_name):
        self.index_name = index_name
        self.client = ElasticConnector().get_client()

    def create_index(self):
        if self.client.indices.exists(index=self.index_name):
            self.client.indices.delete(index=self.index_name)
            print(f"Deleted existing index: {self.index_name}")
        mapping = TextMapping.get_mapping()
        self.client.indices.create(index=self.index_name, body=mapping)
        print(f"Created new index: {self.index_name}")
