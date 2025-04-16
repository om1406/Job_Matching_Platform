import fitz 

def parse_resume(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()

    name = "Candidate"
    skills = extract_skills(text)

    return {
        "name": name,
        "skills": skills,
        "raw_text": text
    }

def extract_skills(text):
    known_skills = ['python', 'sql', 'java', 'machine learning', 'excel', 'communication',
                    'leadership', 'data analysis', 'marketing', 'accounting', 'cloud', 'project management']
    found = [skill for skill in known_skills if skill.lower() in text.lower()]
    return list(set(found))
