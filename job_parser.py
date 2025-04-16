import pandas as pd
from utils import clean_text

def load_jobs(path):
    df = pd.read_csv(path)
    if 'Job Description' not in df.columns:
        raise KeyError("Missing 'Job Description' column in CSV.")
    df['clean_description'] = df['Job Description'].apply(clean_text)
    return df
