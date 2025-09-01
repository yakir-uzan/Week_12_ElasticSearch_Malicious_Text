import pandas as pd
from elasticsearch.helpers import bulk
from app.client import ElasticConnector

class DataLoader:
    def __init__(self, index_name='iran_texts_raw', path='data/tweets_injected.csv'):
        self.index_name = index_name
        self.path = path
        self.client = ElasticConnector().get_client()

    def load_data(self):
        df = pd.read_csv(self.path)
        actions = []
        for inx, row in df.iterrows():
            actions.append({
                "_index": self.index_name,
                "_source": {
                    "TweetID": str(row["TweetID"]),
                    "CreateDate": pd.to_datetime(row["CreateDate"]).strftime("%Y-%m-%dT%H:%M:%S"),
                    "Antisemitic": bool(int(row["Antisemitic"])),
                    "text": row["text"]}})

        success = bulk(self.client, actions)
        print(f"Loaded {success} documents to index '{self.index_name}'")
