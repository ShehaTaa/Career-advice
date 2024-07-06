from flask import Flask, request, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
from src.data_prep import apply_changes
from src.embedder_model import embedder_vector
from src.context_query import get_career_advice
from src.generative_LLM import generate_recommendations

app = Flask(__name__)

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load pre-trained Cross Encoder model
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Load generative model
gen_model = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

# Load job data
file_path = "Data/jobs_data.csv"
job_file = pd.read_csv(file_path)

# Data Preparation and cleansing
job_data = apply_changes(job_file)

# Create vector DB
index = embedder_vector(model, job_data)

@app.route('/get_career_advice', methods=['POST'])
def get_career_advice_api():
    try:
        data = request.get_json()
        query_text = data['query']

        # Get top results based on user query and vector DB
        results = get_career_advice(model, index, job_data, query_text, cross_encoder, top_k=5)

        # Generate personalized career advice
        final_response = generate_recommendations(query_text, results, gen_model)

        return jsonify(final_response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
