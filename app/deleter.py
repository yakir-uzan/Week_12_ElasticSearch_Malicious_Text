from app.client import ElasticConnector

class DocumentDeleter:
    def __init__(self, index_name = "iran_texts_raw"):
        self.client = ElasticConnector().client
        self.index = index_name

    def delete_query(self):
        return {"query": {"bool": {"must": [{"term": {"Antisemitic": False}},
                         {"bool": {"must_not": {"exists": {"field": "weapons"}}}},
                         {"terms": {"sentiment": ["neutral", "positive"]}}]}}}

    def delete_documents(self):
        query = self.delete_query()
        response = self.client.delete_by_query(index = self.index, body= query)
        print(f"[DELETE] Deleted {response['deleted']} documents.")


if __name__ == "__main__":
    deleter = DocumentDeleter()
    deleter.delete_documents()