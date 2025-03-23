import openai
from dotenv import load_dotenv
import os
import json
import re
import shutil
from email_processor import convert_email_to_json
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


def remove_python_cache():
    project_dir = os.path.dirname(os.path.abspath(__file__))      
    for root, dirs, files in os.walk(project_dir):
        # Remove __pycache__ directories
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_dir = os.path.join(root, dir_name)
                print(f"Removing directory: {cache_dir}")
                shutil.rmtree(cache_dir)

        # Remove .pyc files
        for file_name in files:
            if file_name.endswith(".pyc"):
                pyc_file = os.path.join(root, file_name)
                print(f"Removing file: {pyc_file}")
                os.remove(pyc_file)


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

def process_and_classify_emails():
    """
    Process and classify emails from the 'unread' directory.
    """
    try:       
        # List all files in the directory
        remove_python_cache()
        email_files = read_unread_mailBox()
        file_names = [os.path.basename(file) for file in email_files]

        # Process and classify each email
        email_results = []
        for email_file in email_files:
            email_content = convert_email_to_json(email_file)
            updated_email_content = ""
            if "classify_content" in email_content:
                updated_email_content = re.sub(r"[^a-zA-Z0-9\s]", "", email_content["classify_content"])
                                  
            classification = classify_content(updated_email_content, model=model)
            classification["email_subject"] = email_content["subject"]
            email_results.append(classification)

        # Move processed files to the 'processed' folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        source_folder = os.path.abspath(os.path.join(current_dir, "..", "mail_dropbox", "unread"))
        destination_folder = os.path.abspath(os.path.join(current_dir, "..", "mail_dropbox", "processed"))
        move_read_files(source_folder, destination_folder,file_names)
    
        return email_results

    except Exception as e:
        return f"Error: {e}"

def classify_content(prompt, model="gpt-4o-mini"):
    try:
        # Function to process nested sub-request types
        def process_sub_request_types(sub_request_types):
            result = []
            for sub_request in sub_request_types:
                if isinstance(sub_request, dict):  # Handle nested sub-request types
                    result.append(f"{sub_request['type']}: {', '.join(sub_request['subRequestTypes'])}")
                else:
                    result.append(sub_request)
            return result

        # Generate request types string dynamically
        request_types_list = request_types["CommercialBankLendingService"]["RequestTypes"]
        request_types_str = "\n".join(
            [f"{req['type']}: {', '.join(process_sub_request_types(req['subRequestTypes']))}" for req in request_types_list]
        )

        
        # Define the prompt for classification
        classification_prompt = f"""
        You are a classification assistant. Analyze the following content and classify it into:
        - Request Type
        - Request Subtype
        - Confidence Score
        possible request types and subtypes.
        Based on the following possible request types and subtypes:
        {request_types_str}

        Content: "{prompt}"

        Respond in the following JSON format:
        {{
            "Request": [
                {{
                    "request_type": "<type>",
                    "request_subtype": "<subtype>",
                    "confidence_score": <score>,
                    "reasoning": "<reasoning>"
                }}
            ]            
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
    
        raw_result = completion.choices[0].message["content"]

        cleaned_result = raw_result.strip("```").strip("json").strip()

        # Convert the cleaned string to a JSON object
        result = json.loads(cleaned_result)
        for request in result["Request"]:
            request["confidence_score"] = float(request["confidence_score"])*100
            
        return result

    except Exception as e:
        return {"error": str(e)}

def read_unread_mailBox():
    """
    Reads all files from the 'unread' directory and processes them.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        email_path = os.path.abspath(os.path.join(current_dir,"..", "mail_dropbox", "unread"))

        # Check if the directory exists
        if not os.path.exists(email_path):
            return f"Error: Directory '{email_path}' does not exist."

        # List all files in the directory
        email_files = [os.path.join(email_path, file) for file in os.listdir(email_path) if os.path.isfile(os.path.join(email_path, file))]

        return email_files

    except Exception as e:
        return f"Error: {e}"

def move_read_files(source_folder, destination_folder, file_names):
    """
    Moves specified files from the source folder to the destination folder.
    :param source_folder: Path to the source folder.
    :param destination_folder: Path to the destination folder.
    :param file_names: List of file names to move.
    """
    try:
        # Ensure the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Move each specified file
        for file_name in file_names:
            source_file = os.path.join(source_folder, file_name)
            destination_file = os.path.join(destination_folder, file_name)

            if os.path.exists(source_file):
                shutil.move(source_file, destination_file)
                print(f"Moved file: {source_file} -> {destination_file}")
            else:
                print(f"File not found: {source_file}")

        return f"Successfully moved {len(file_names)} files to '{destination_folder}'."

    except Exception as e:
        return f"Error while moving files: {e}"
# Example usage
if __name__ == "__main__":
    prompt = "how to read emails from outlook?"
    response = process_and_classify_emails()
    print(response)