from config import client

def ask_openai(query, chunks, compare_mode=False):
    combined_text = "\n\n".join(chunks)
    
    if compare_mode:
        prompt = f"""Compare and contrast the following excerpts from two different FOMC minutes:

{combined_text}

Please analyze the key differences and similarities regarding:
1. Economic conditions
2. Policy decisions
3. Forward guidance
4. Risk assessments

Focus on: {query}"""
    else:
        prompt = f"""Based on the following excerpts from FOMC minutes:

{combined_text}

Please provide a detailed and accurate answer to this question:
{query}

If the provided excerpts don't contain enough information to fully answer the question, please state that explicitly."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in monetary policy and Federal Reserve operations. Provide accurate, nuanced answers based only on the provided FOMC minutes excerpts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()