import openai
from dotenv import load_dotenv
import os
import json
import re
import time
from duplicate_mail_validation import is_duplicate
from trained_model import  classification_Prompt
import shutil
from email_processor import convert_email_to_json
# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

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


def process_and_classify_emails():
    """
    Process and classify emails from the 'unread' directory.
    """
    try:       
        # List all files in the directory
        remove_python_cache()
        email_files = read_unread_mailBox()
        file_names = [os.path.basename(file["file_name"]) for file in email_files]
        
        # Process and classify each email
        email_results = []
        for email_file in email_files:
            email_content = convert_email_to_json(email_file["file_name"])

            is_duplicate_email = is_duplicate(email_content) 
            if is_duplicate_email:
                print(f"Skipping duplicate email: {email_content['message_id']}")
                email_file["is_duplicate"] = True
                continue  # Skip processing this email if it's a duplicate
                                
            classification = classify_content(email_content["classify_content"])
            classification["email_subject"] = email_content["subject"]
            email_results.append(classification)
            add_to_classified_mail(email_content)
        # Move processed files to the 'processed' folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        source_folder = os.path.abspath(os.path.join(current_dir, "..", "mail_dropbox", "unread"))
        destination_folder = os.path.abspath(os.path.join(current_dir, "..", "mail_dropbox", "processed"))
        move_read_files(source_folder, destination_folder,file_names)
        
        return email_results

    except Exception as e:
        return f"Error: {e}"

def classify_content(prompt):
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
        classification_prompt = classification_Prompt(prompt,request_types_str) 
        
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
        # Add detailed reasoning for each request
        for request in result["Request"]:            
            # Convert confidence score to percentage
            request["confidence_score"] = float(request["confidence_score"])
           
        
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
        file_list = []
        for file in email_files:
            file_list.append({"file_name":file,"is_duplicate":False})
        return file_list

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
                move_file_with_retry(source_file, destination_file)               
            else:
                print(f"File not found: {source_file}")

        return f"Successfully moved {len(file_names)} files to '{destination_folder}'."

    except Exception as e:
        return f"Error while moving files: {e}"

def move_file_with_retry(source_file, destination_file, retries=3, delay=2):
    for attempt in range(retries):
        try:
            shutil.move(source_file, destination_file)
            print(f"Moved file: {source_file} -> {destination_file}")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print(f"Failed to move file after {retries} attempts: {source_file}")

def add_to_classified_mail(email_content):
    """
    Adds the email content to the classified_mail.json file.
    :param email_content: The email content to add.
    :param json_file_path: Path to the classified_mail.json file.
    """
    try:
        try:
            json.dumps(email_content)  # This will raise an error if email_content is not serializable
        except (TypeError, ValueError) as e:
            return f"Invalid email content: {e}"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir,"dataset","db_data","classified_mail.json")

        # Check if the JSON file exists
        if os.path.exists(json_file_path):
            # Load existing data
            with open(json_file_path, "r") as file:
                data = json.load(file)
        else:
            # Initialize an empty list if the file does not exist
            data = []

        # Append the new email content
        data.append(email_content)

        # Write the updated data back to the file
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Email content added to {json_file_path}")
        return f"Email content successfully added to {json_file_path}."

    except Exception as e:
        return f"Error while adding email content to {json_file_path}: {e}"



# Example usage
if __name__ == "__main__":
    prompt = "how to read emails from outlook?"
    response = process_and_classify_emails()
    print(response)