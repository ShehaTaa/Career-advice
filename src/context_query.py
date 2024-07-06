import numpy as np
import pandas as pd

# Method to get career advice
def get_career_advice(model, index, job_data, query_text, cross_encoder, top_k=5):

    '''
    args:
        model: SentenceTransformer model object to encode the user query
        index: vector db that has the indexed embedding sentences 
        job_data: preparation data dataframe
        query_text: string user query
        cross_encoder: re-ranking model 
        top_k : top k documents related to user query
    return
        dataframe has the top ranked documents 
    '''
    # Encode query
    query_embedding = model.encode(query_text)
    query_embedding = np.expand_dims(query_embedding, axis=0)

    # Search in FAISS index
    scores, indices = index.search(query_embedding, top_k)

    # Retrieve job postings
    pred_list = list(indices[0])
    pred_strings_list = [job_data['job_details'].iloc[item] for item in pred_list]

    # Prepare input for cross-encoder
    cross_input_list = [[query_text, pred_text] for pred_text in pred_strings_list]

    # Score all retrieved passages using the cross_encoder
    cross_scores = cross_encoder.predict(cross_input_list)

    # Create DataFrame with results and scores
    df = pd.DataFrame(cross_input_list, columns=['query_text', 'pred_text'])
    df['original_index'] = pred_list
    df['cross_scores'] = cross_scores

    # Sort the DataFrame in descending order based on the scores
    df_sorted = df.sort_values(by='cross_scores', ascending=False).reset_index(drop=True)

    return df_sorted.head(top_k)