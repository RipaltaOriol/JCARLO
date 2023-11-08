import streamlit as st
import numpy as np
import time
import pandas as pd

st.set_page_config(
    page_title="JCarlo",
    page_icon="📝",
)

def minMax(x):
    return pd.Series(index=['min','max'],data=[x.min().astype("float16"),x.max()])


st.write("# Welcome to JCarlo! 👋")

# st.sidebar.success("Select a model from above.")

st.markdown(
    """
    JCarlo aims to be an AI tool able to find research sources from user prompts.
"""
)

st.markdown("## Ranking System")

st.markdown("Once we obtain a list of results referred as candidates, 10 in this case. We process to rank them in relative terms. This means ranking them relative to one another and not in absolute terms to all other papers out there.")

st.markdown("### Current Formula")
st.latex(r'''
Embedding\:Score \:*\: 0.5 \:+\: Release\:Year \:*\: 0.2 \:+\: Citations\:Number \:*\: 0.3''')

st.markdown("### Normalising Year and Citations Score")

st.markdown("To normalise integer numbers we will use an exponential ranking system with bases of 2 such as:")

score = np.array(range(10, 0, -1))

raw_scores = pd.DataFrame({"Score Base .2": score, "Score Base .3": score, "Score Base .5": score})
raw_scores['Score Base .2'] = raw_scores['Score Base .2'].apply(lambda x: pow(x, 0.2))
raw_scores['Score Base .3'] = raw_scores['Score Base .3'].apply(lambda x: pow(x, 0.3))
raw_scores['Score Base .5'] = raw_scores['Score Base .5'].apply(lambda x: pow(x, 0.5))
raw_scores.index += 1 

chart_scores = st.line_chart(raw_scores)

st.markdown("After we get a ranking score we will normalise these values to get an output between 0 and 1 using the following formula:")

st.latex(r'''z_i = \frac{x_i – \min(x)}{\max(x) – \min(x)}''')

st.markdown("""
    where:

    * zi: The ith normalized value in the dataset
    * xi: The ith value in the dataset
    * min(x): The minimum value in the dataset
    * max(x): The maximum value in the dataset
""")

st.markdown("#### Final Scores")

min_max = raw_scores.apply(minMax)

normalised_scores = pd.DataFrame()

for col in raw_scores.columns:
    normalised = raw_scores[col].apply(lambda x: (x - min_max.loc['min', col])/(min_max.loc['max', col] - min_max.loc['min', col]))
    normalised_scores[col] = normalised

chart_normal = st.line_chart(normalised_scores)

st.markdown("## Testing")
st.markdown(f"""Test are located in `/tests` folder and each of them contain an object with its query, target paper and paper year.
During testing points will be awarded to a model/prototype depending on where does the solution appear in the results.

_Notes_:   
* More tests are needed
* In the long-run it would be better to store an ID to reference the target paper
* This testing scoring method is provisionary
""")

st.markdown("#### Testing Scores")
testing_chart = pd.DataFrame(
   {
       "Result #": [1, 2, 3],
       "Testing Points": [5, 3, 1],
   }
)

st.bar_chart(testing_chart, y="Testing Points", x="Result #")
