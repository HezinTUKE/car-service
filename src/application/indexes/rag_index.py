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
            }
        },
    }
