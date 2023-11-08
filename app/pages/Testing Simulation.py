from pysondb import db
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Testing Simulator", page_icon="🥼")
st.sidebar.header("Tesing Simulator 🥼")

performanceDb = db.getDb("local_db/performance.json")
testsDb = db.getDb("local_db/tests.json")
perf_prot_0 = performanceDb.getByQuery(query={'name': "prototype0"})
perf_plain = performanceDb.getByQuery(query={'name': "plain_cosinus"})


st.markdown("# Testing Simulator 🥼")
st.markdown("This page analyses the results from prototype simulations")

tests = testsDb.getAll()

scores = {
    "prototype0": [],
    "plain_cosinus": [],
}

score_index = []

# NOTE: this code is not stable

for model in ['prototype0', 'plain_cosinus']:
    items = perf_prot_0 if model == 'prototype0' else perf_plain

    

    for item in items:

        if model == 'prototype0':
            score_index.append(item['query'])

        test = testsDb.getByQuery(query={"query": item['query']})[0]

        df = pd.read_json(item['results'], orient="records")
        
        test_score = 0
        for idx, row in enumerate(df.head(3).itertuples()):
            
            if row.title == test['sol']:
                print(idx, row.title, item['query'], model)
                if idx == 0:
                    test_score = 5
                elif idx == 1:
                    test_score = 3
                elif idx == 2:
                    test_score = 1
            
        
        scores[model].append(test_score)


st.markdown("## Overall Comparative")


chart_comparative = pd.DataFrame(scores, columns=['prototype0', "plain_cosinus"], index=score_index)
st.bar_chart(chart_comparative)
    
st.markdown("### Prototype 0 Details")

for item in perf_prot_0:

    def highlight_answer(s):
        q = {"query": item['query']}
        test = testsDb.getByQuery(query=q)[0]
        return ['background-color: yellow']*len(s) if s.title == test['sol'] else ['background-color: white']*len(s)

    st.markdown(f"#### :blue[{item['query']}]")

    df = pd.read_json(item['results'], orient="records")
    st.dataframe(
        df.style.apply(highlight_answer, axis=1),
        column_config={
            "doi": None,
            "year_ref": None,
            "citation_ref": None,
        },
        column_order=("title", "final", "embedding_score", "year_norm", "citation_norm", "year", "citations"),
        hide_index=True,
    )

st.divider()

st.markdown("### Plain Cosinus Details")

for item in perf_plain:

    def highlight_answer(s):
        q = {"query": item['query']}
        test = testsDb.getByQuery(query=q)[0]
        return ['background-color: yellow']*len(s) if s.title == test['sol'] else ['background-color: white']*len(s)

    st.markdown(f"#### :blue[{item['query']}]")

    df = pd.read_json(item['results'], orient="records")
    st.dataframe(
        df.style.apply(highlight_answer, axis=1),
        column_config={
            "doi": None,
            "year_ref": None,
            "citation_ref": None,
        },
        column_order=("title", "final", "embedding_score", "year_norm", "citation_norm", "year", "citations"),
        hide_index=True,
    )
