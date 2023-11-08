def get_raw_score(df):
    scores = [pow(score, 0.5) for score in range(len(df.index), 0, -1)]

    df.sort_values(by=['year'], inplace=True)
    df['year_ref'] = scores

    df.sort_values(by=['citations'], ascending=False, inplace=True)
    df['citation_ref'] = scores

    return df

def get_normalised_score(df):
    df['year_norm'] = df['year_ref'].apply(lambda x: (x - df['year_ref'].min())/(df['year_ref'].max() - df['year_ref'].min()))
    df['citation_norm'] = df['citation_ref'].apply(lambda x: (x - df['citation_ref'].min())/(df['citation_ref'].max() - df['citation_ref'].min()))

    return df

def get_final_score(df):
    df['final'] = df['embedding_score'] * 0.5 + df['year_norm'] * 0.2 + df['citation_norm'] * 0.3
    
    return df