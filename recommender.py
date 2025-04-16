import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_jobs_bert(resume_text, job_df, top_n=5, stream=None):
    if stream and stream != "All":
        job_df = job_df[job_df['Stream'].str.lower() == stream.lower()]

    if job_df.empty:
        return pd.DataFrame()

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    resume_inputs = tokenizer(resume_text, return_tensors='pt', truncation=True, padding=True)
    job_inputs = tokenizer(list(job_df['clean_description']), return_tensors='pt', truncation=True, padding=True)

    with torch.no_grad():
        resume_embed = model(**resume_inputs).last_hidden_state.mean(dim=1)
        job_embeds = model(**job_inputs).last_hidden_state.mean(dim=1)

    scores = cosine_similarity(resume_embed.numpy(), job_embeds.numpy())[0]
    job_df['Match Score'] = (scores * 100).round(2)

    return job_df.sort_values('Match Score', ascending=False).head(top_n)[
        ['Job Title', 'Industry', 'Required Skills', 'Job Description', 'Stream', 'Match Score']
    ]
