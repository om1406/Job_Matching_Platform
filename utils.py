import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text.lower()

def generate_skill_gap(job_df, user_skills):
    all_required = set(
        skill.strip().lower()
        for skills in job_df['Required Skills'].dropna().str.split(',')
        for skill in skills
    )
    user = set(skill.lower() for skill in user_skills)
    return all_required & user, all_required - user
