import streamlit as st

import numpy as np

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd
from pysondb import db

import gc
import os
import faiss

from pipeline.fetch_metadata import merge_metadata, fetch_metadata
from pipeline.compute_scores import get_raw_score, get_normalised_score, get_final_score

index_name = "papers2"

st.set_page_config(page_title="Protoype 0", page_icon="🧪")
st.sidebar.header("Prototype 0 🧪")


try:
    es = Elasticsearch(
        "https://localhost:9200/",
        basic_auth=("elastic", "Z1*nfDFd1YhmgLg8w1qo"),
        ca_certs="/Users/uri/Desktop/Dev/elasticsearch-8.10.4/config/certs/http_ca.crt"
    )
except ConnectionError as e:
    print("Connection error:", e)

if es.ping():
    print("Succesfully connected to ElasticSearch!")
else:
    print("Oops! Cannot connect to ElasticSearch!")

def search(input_keyword):
    model = SentenceTransformer('msmarco-distilbert-base-v4')
    input_embedding = model.encode(input_keyword)

    query = {
        "field": "vector",
        "query_vector": input_embedding,
        "k": 10,
        "num_candidates": 500
    }

    res = es.knn_search(index=index_name, knn=query, source=["title", "doi", "abstract"])

    reference = [target  for target in res['hits']['hits']]

    pipeline_df = pd.DataFrame()

    for ref in reference:
        source = ref['_source']
        print(ref)
        new_ref = {'title': source['title'], 'doi': source['doi'], "embedding_score": ref['_score']}
        pipeline_df = pipeline_df.append(new_ref, ignore_index=True)

    
    return pipeline_df

def transform_results(df, query):
    papers_dois = df['doi'].tolist()
    metadata = fetch_metadata(papers_dois)
    pipeline_df = merge_metadata(df, metadata)
    pipeline_df = get_raw_score(pipeline_df)
    pipeline_df = get_normalised_score(pipeline_df)
    pipeline_df = get_final_score(pipeline_df)
    
    pipeline_df.sort_values(by=['final'], ascending=False, inplace=True)

    # save results to DB
    # dbase = db.getDb("local_db/performance.json")
    # data = pipeline_df.to_json(orient="records")
    # dbase.add({"name":"prototype0","query": query, "results": data})

    return pipeline_df


def main():
    st.title("JCarlo AI Prototype 0 🧪")
    

    search_query = st.text_input("Search a paper")

    if st.button("Search"):

        if search_query:
            results = search(search_query)
            results = transform_results(results, search_query)

            st.markdown("**Results**:")


            for row in results.itertuples():
                with st.container():
                    try:
                        st.markdown(f"#### {row.title}")
                    except Exception as e:
                        print(e)
                    try:
                        st.write(f":blue[{round(row.final, 4)}]")
                    except Exception as e:
                        print(e)
                    st.divider()

if __name__ == "__main__":
    main()