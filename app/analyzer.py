from app.client import ElasticConnector
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re

nltk.download("vader_lexicon")

class TextAnalyzer:
    def __init__(self, index_name, weapons_file_path):
        self.client = ElasticConnector().get_client()
        self.sia = SentimentIntensityAnalyzer()
        self.weapons_list = self.load_file(weapons_file_path)

    """ טעינת הקובץ והכנתו לאנאליזה """
    def load_file(self, weapons_file_path):
        with open(weapons_file_path, 'r', encoding="utf-8") as f:
            weapons_list = [w.strip().lower() for w in f.readlines() if w.strip()]
        return weapons_list

    """ מציאת הרגש בטקסט """
    def found_sentiment(self, text):
        score = self.sia.polarity_scores(text)["compound"]
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"

    """ מציאת נשקים בטקסט """
    def found_weapons(self, text):
        words = re.findall(r"\b\w+\b", text.lower())
        return list(set(word for word in words if word in self.weapons_list))

    """ הוספת עמודות רגש וכלי נשק לקובץ המקורי """
    def enrich_documents(self, index_name, size = 10000):
        result = self.client.search(index= index_name, size= size, query= {"match_all": {}})
        hits = result["hits"]["hits"]

        for doc in hits:
            doc_id = doc["_id"]
            text = doc["_source"].get("text", "")
            sentiment = self.found_sentiment(text)
            weapons_found = self.found_weapons(text)

            update_body = {"doc": {"sentiment": sentiment}}
            if weapons_found:  # רק אם נמצאו נשקים
                update_body["doc"]["weapons"] = weapons_found

            self.client.update(index=index_name, id=doc_id, body=update_body)
        print(f"Updated {len(hits)} documents with sentiment & weapons.")