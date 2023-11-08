import requests

API_KEY = "ijZAh3FxuM1YXwVYvuFgBAm2xreyRcu5KSNxaqFa"

def fetch_metadata(papers_dois=[]):
    ids = [f"DOI:{doi}" for doi in papers_dois]

    response = requests.post(f"https://api.semanticscholar.org/graph/v1/paper/batch",
        headers={'X-API-KEY': API_KEY},
        params={'fields': 'title,url,year,citationCount,abstract,externalIds'},
        json={"ids": ids}
    )

    metadata = {}

    if  response.status_code == 200:
        data = response.json()
        for paper in data:
            # brining the DOI forward as object keys and set the DOI to lower case
            metadata[paper['externalIds']['DOI'].lower()] = paper
        
        return metadata

def merge_metadata(df, metadata):
    df['year'] = df['doi'].apply(lambda x: metadata[x]['year'])
    df['citations'] = df['doi'].apply(lambda x: metadata[x]['citationCount'])
    return df