import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini";

def get_classify(prompt, model="gpt-4o-mini"):
   
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    prompt = "how to read emails from outlook?"
    response = get_chat_completion(prompt)
    print(response)