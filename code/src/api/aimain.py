import openai
from dotenv import load_dotenv
import os
import json
# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini";

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = "".join([current_dir, "\\dataset\\request-type.json"])
# Load the JSON file
with open(json_file_path, "r") as file:
    request_types = json.load(file)

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


def classify_content(prompt, model="gpt-4o-mini"):
    try:
        request_types_str = "\n".join(
            [f"{req_type}: {', '.join(subtypes)}" for req_type, subtypes in request_types.items()]
        )
        print(request_types_str)
        # Define the prompt for classification
        classification_prompt = f"""
        You are a classification assistant. Analyze the following content and classify it into:
        - Request Type
        - Request Subtype
        Based on the following possible request types and subtypes:
        {request_types_str}

        Content: "{prompt}"

        Respond in the following JSON format:
        {{
            "request_type": "<type>",
            "request_subtype": "<subtype>",
            "confidence_score": <score>,
            "reasoning": "<reasoning>"
        }}
        """

        # Call OpenAI's ChatCompletion API
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": classification_prompt}
            ]
        )

        # Extract the response content
        result = completion.choices[0].message["content"]
        return result

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    prompt = "how to read emails from outlook?"
    response = get_classify(prompt)
    print(response)