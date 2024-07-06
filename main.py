import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline

from src.data_prep import apply_changes
from src.embedder_model import embedder_vector
from src.context_query import get_career_advice
from src.generative_LLM import generate_recommendations

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load pre-trained Cross Encoder model
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Load generative model
gen_model = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

# User query
query_text = "Machine Learning Engineer"

# 1. Read data
file_path = "Data/jobs_data.csv"
job_file = pd.read_csv(file_path)

# 2. Data Preparation and cleansing
job_data = apply_changes(job_file)

# 3. load Embedder and create vector DB
index = embedder_vector(model, job_data)

# 4. return top results based on user query and vector DB 
results = get_career_advice(model, index, job_data, query_text, cross_encoder, top_k=5)

# 5. Generative model to generate personalized career advice
final_response = generate_recommendations(query_text, results, gen_model)




