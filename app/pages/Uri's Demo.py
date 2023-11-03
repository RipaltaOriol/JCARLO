import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import gc
import os
import faiss


index_name = "papers"

# DATA_SOURCE = "/Users/uri/Desktop/Projects/JCARLO/demo_01/my_library.csv"
# data = pd.read_csv(DATA_SOURCE, memory_map=True)
# df = data[['title','abstract']]
# del data

# gc.collect()

# df.dropna(inplace=True)
# df.drop_duplicates(subset=['abstract'],inplace=True)

st.set_page_config(page_title="Uri's Demo", page_icon="👨🏻‍💻")

st.sidebar.header("Uri's Demo")


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
        "k": 5,
        "num_candidates": 500
    }

    res = es.knn_search(index="papers", knn=query, source=["title", "abstract"])
    results = res["hits"]['hits']
    return results

# def fetch_papers_info(dataframe_idx):
#     info = df.iloc[dataframe_idx]
#     meta_dict = {}
#     meta_dict['title'] = info['title']
#     return meta_dict
    
def search_dot(query, top_k):
    model_dot = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')
    query_vector = model_dot.encode([query])
    try:
        index_loaded = faiss.read_index("/Users/uri/Desktop/Projects/JCARLO/demo_01/papers.index")
    except:
        print("Something went wrong")
    finally:
        print("This step would search for the query/result")
        # top_k = index_loaded.search(query_vector, top_k)
    
    
    # top_k_ids = top_k[1].tolist()[0]
    # top_k_ids = list(np.unique(top_k_ids))
    # results =  [fetch_papers_info(idx) for idx in top_k_ids]
    return "Results"
    return results

def main():
    st.title("Search Papers using Assymetrical Semantic Search")
    st.caption("Model msmarco-distilbert-base-v4 fine tuned for cosine similarity")
    st.caption("Model msmarco-distilbert-base-dot-prod-v3 fine tuned for dot-plot similarity")

    radio_model = st.radio(
    "Model to use",
    ("msmarco-distilbert-base-dot-prod-v3", "msmarco-distilbert-base-v4"),
    )

    if radio_model == "msmarco-distilbert-base-dot-prod-v3":
        st.text("Dot-plot similarity")
    elif radio_model == "msmarco-distilbert-base-v4":
        st.text("Cosine similarity")

    search_query = st.text_input("Search a paper")

    if st.button("Search"):

        if radio_model == "msmarco-distilbert-base-dot-prod-v3":
            if search_query:
                results = search_dot(search_query, top_k=5)
                st.write("This model demo doesn't work - Python 3.8 required")
   
        elif radio_model == "msmarco-distilbert-base-v4":
            if search_query:
                results = search(search_query)

                st.subheader("Results")

                for res in results:
                    with st.container():
                        if "_source" in res:
                            try:
                                st.header(f"{res['_source']['title']}")
                            except Exception as e:
                                print(e)
                            try:
                                st.write(f"{res['_source']['abstract']}")
                            except Exception as e:
                                print(e)
                            st.divider()

if __name__ == "__main__":
    main()