import streamlit as st
import requests


st.set_page_config(page_title="Semantic Scholar Demo", page_icon="🔬")

st.markdown("# Semantic Scholar API")
st.sidebar.header("Semantic Scholar API")
st.write(
    """This page shows how Semantic Scholar API works on a basic level. There are some more customization that can be done to these requests although some heavy limitations too!"""
)

API_KEY = "ijZAh3FxuM1YXwVYvuFgBAm2xreyRcu5KSNxaqFa"

# query = "Mitochondrial metabolism promotes adaptation to proteotoxic stress"

query = st.text_input("Search a paper")

if st.button("Search"):
    if query:
        rsp = requests.get('https://api.semanticscholar.org/graph/v1/paper/search',
            headers={'X-API-KEY': API_KEY},
            params={'query': query, 'limit': 5, 'fields': 'title,url,year,citationCount,abstract'})

        if  rsp.status_code == 200:

            data = rsp.json()
            if 'data' in data:
                for paper in data['data']:
                    st.markdown(f"### {paper['title']}")
                    st.caption(f"Year: :blue[{paper['year']}]")
                    st.caption(f"Citations count: :blue[{paper['citationCount']}]")
                    if paper['abstract']:
                        st.write(paper['abstract'])
                    else:
                        st.write(":red[Abstract not available.]")
                    st.divider()
            else:
                st.write(":red[No results found :(]")




