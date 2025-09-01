from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch("http://localhost:9200")
index_name = "iran_texts_raw"

@app.get("/")
def home():
    return "hello Kodcodist!!!"


def is_data_processed():
    """ בודק אם קיימים מסמכים עם שדות רגש ונשק """
    query = {"query": {"exists": {"field": "sentiment"}}}
    response = es.count(index=index_name, body=query)
    return response["count"] > 0


@app.get("/antisemitic_with_weapons")
def get_antisemitic_with_weapons():
    """ מחזיר את כל המסמכים שהם גם אנטישמיים וגם כוללים כלי נשק """
    if not is_data_processed():
        return {"message": "Data has not been processed yet."}

    query = {"query": {"bool": {"must": [{"term": {"Antisemitic": True}},{"exists": {"field": "weapons"}}]}},"size": 10000}
    response = es.search(
        index=index_name,
        query=query["query"],
        size=query["size"])
    results = [hit["_source"] for hit in response["hits"]["hits"]]
    return results


@app.get("/documents_with_two_weapons")
def get_documents_with_two_weapons():
    if not is_data_processed():
        return {"message": "Data has not been processed yet."}

