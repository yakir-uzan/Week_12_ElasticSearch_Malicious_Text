class TextMapping:
    @staticmethod
    def get_mapping():
        return {
            "mappings": {
                "properties": {
                    "TweetID": {"type": "keyword"},
                    "CreateDate": {"type": "date"},
                    "Antisemitic": {"type": "boolean"},
                    "text": {"type": "text"}
                }
            }
        }
