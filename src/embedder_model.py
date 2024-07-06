import numpy as np
import faiss

# method to create document embedding and the vector DB
def embedder_vector (model,job_data):
    '''
    args:
        model: SentenceTransformer model object
        job_data: preparation data dataframe
    return
        ready to use vector db 
    '''
    # Encode the combined job details into dense vectors
    job_data['embeddings'] = job_data['job_details'].apply(lambda x: model.encode(x))

    # Convert embeddings to a numpy array
    job_embeddings = np.vstack(job_data['embeddings'].values)

    print(f"Number of job embeddings: {len(job_embeddings)}")
    print(f"Embedding dimension: {job_embeddings.shape}")

     ### Create vector database object
    vector_db = vector_index(job_embeddings)
    return(vector_db)

# Create vector database object
def vector_index(job_embeddings):
    '''
    args:
        job_embeddings: numpy array of embedding sentences
    return
        ready to use vector db 
    '''
    embed_length = job_embeddings.shape[1]
    index = faiss.IndexFlatL2(embed_length)
    # Check if the index is trained.
    # No training needed when using greedy search i.e. IndexFlatL2
    # print(index.is_trained)

    # Add the embeddings to the index
    return(index.add(job_embeddings))
    