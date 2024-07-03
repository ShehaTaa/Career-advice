import pandas as pd

##read data
file_path = "Data/jobs_data.csv"
jop_df = pd.read_csv(file_path)


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


# Clean the 'description' and 'requirements' columns
jop_df['description'] = jop_df['description'].apply(clean_text)
jop_df['requirements'] = jop_df['requirements'].apply(clean_text)

# Function to concatenate columns with specified format
def concatenate_columns(row):
    return f"[job_title] {row['job_title']} [description] {row['description']} [requirements] {row['requirements']} [career_level] {row['career_level']}"

# Create the new 'job_details' column
jop_df['job_details'] = jop_df.apply(concatenate_columns, axis=1)
