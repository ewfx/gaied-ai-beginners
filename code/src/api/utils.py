import json
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

def get_classify(prompt):
   
    try:
        # Call OpenAI's ChatCompletion API
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
    
        raw_result = completion.choices[0].message["content"]

        cleaned_result = raw_result.strip("```").strip("json").strip()

        # Convert the cleaned string to a JSON object
        result = json.loads(cleaned_result)
        return result
    except Exception as e:
        return f"An error occurred: {e}"