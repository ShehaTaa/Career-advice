import pandas as pd
from bs4 import BeautifulSoup
import re



# Function to clean text
def clean_text(text):
    if isinstance(text, str):
        # Remove HTML tags
        cleaned_text = BeautifulSoup(text, 'html.parser').get_text()
        # Remove extra whitespace and normalize line breaks
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        # Remove unnecessary punctuation
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
        # Remove leading and trailing spaces
        cleaned_text = cleaned_text.strip()
        return cleaned_text
    else:
        return text

# Function to concatenate columns with specified format
def concatenate_columns(row):
    return f"[job_title] {row['job_title']} [description] {row['description']} [requirements] {row['requirements']} [career_level] {row['career_level']}"

def apply_changes(job_data):
    # Clean the 'description' and 'requirements' columns
    job_data['description'] = job_data['description'].apply(clean_text)
    job_data['requirements'] = job_data['requirements'].apply(clean_text)

    # Create the new 'job_details' column
    job_data['job_details'] = job_data.apply(concatenate_columns, axis=1)

    return job_data
# job_data.to_csv("/content/saved_dataset/job_data_processed.csv", index=False)
