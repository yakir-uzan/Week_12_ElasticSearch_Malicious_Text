from app.client import ElasticConnector
from app.indexer import Indexer
from app.loader import DataLoader
from app.analyzer import TextAnalyzer
from app.deleter import DocumentDeleter

def main():
    index_name = "iran_texts_raw"
    csv_path = "data/tweets_injected.csv"
    weapons_path = "data/weapons.txt"

    print("[1] Connecting to Elasticsearch...")
    client = ElasticConnector().get_client()
    print("Connection established!")

    print("\n[2] Deleting and creating a fresh index...")
    indexer = Indexer(index_name=index_name)
    indexer.create_index()
    print("Index created!")

    print("\n[3] Loading data from CSV into Elasticsearch...")
    loader = DataLoader(index_name=index_name)
    loader.load_data()
    print("Data loaded successfully!")

    print("\n[4] Enriching documents with sentiment and weapons detection...")
    analyzer = TextAnalyzer(index_name=index_name, weapons_file_path=weapons_path)
    analyzer.enrich_documents(index_name=index_name)
    print("Documents enriched successfully!")

    print("\n[5] Deleting documents that are not antisemitic, have no weapons, and have positive/neutral sentiment...")
    deleter = DocumentDeleter(index_name=index_name)
    deleter.delete_documents()
    print("Irrelevant documents deleted!")

    print("\n All steps completed successfully.")

if __name__ == "__main__":
    main()
