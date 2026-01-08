from application.indexes.base_index import BaseIndex
from application.enums.services.indexes import OpensearchIndexes


class RagIndex(BaseIndex):
    index = OpensearchIndexes.RAG_INDEX.value

    __mapping__ = {
        "settings": {"index": {"knn": True}},
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 768,
                    "method": {"name": "hnsw", "space_type": "cosinesimil", "engine": "nmslib"},
                },
                "source": {"type": "keyword"},
                "name": {"type": "text"},
                "point": {"type": "geo_point"},
                "city": {"type": "keyword"},
                "country": {"type": "keyword"},
                "offers": {
                    "type": "nested",
                    "properties": {
                        "base_price": {"type": "float"},
                        "sale": {"type": "integer"},
                        "currency": {"type": "keyword"},
                        "offer_type": {"type": "keyword"},
                        "car_compatibilities": {
                            "type": "nested",
                            "properties": {
                                "car_type": {"type": "keyword"},
                                "car_brand": {"type": "keyword"},
                            },
                        },
                    },
                },
            }
        },
    }
