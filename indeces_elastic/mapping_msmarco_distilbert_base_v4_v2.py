index_mapping = {
    "properties": {
        "title": {
            "type": "text"
        },
        "doi": {
            "type": "text"
        },
        "abstract": {
            "type": "text"
        },
        "doc_len": {
            "type": "long"
        },
        "vector": {
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "cosine"
        }
    }
}