index_mapping = {
    "properties": {
        "Release Year": {
            "type": "long"
        },
        "Title": {
            "type": "text"
        },
        "Origin/Ethnicity": {
            "type": "text"
        },
        "Director": {
            "type": "text",
        },
        "Genre": {
            "type": "text",
        },
        "Wiki Page": {
            "type": "text"
        },
        "Plot": {
            "type": "text"
        },
        "vector": {
            "type": "dense_vector",
            "dims": 384,
            "index": True,
            "similarity": "l2_norm"
        }
    }
}