
def generate_recommendations(query, job_results, gen_model):

    '''
    args:
        query: string user query
        job_results: preparation data dataframe
        gen_model: hugging face text-generation model LLM      
    return
        string user related advice genereted from LLM
    '''
    prompt = f"User query: {query}\n\nRelevant Conext:\n"
    for _, job in job_results.iterrows():
        prompt += f"{job['pred_text']}\n\n"

    prompt += f"Based on your interest in the role of {query}, here are some personalized career advice:"

    response = gen_model(prompt, max_new_tokens=200)
    return response[0]['generated_text']