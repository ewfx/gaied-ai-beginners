from email.parser import BytesParser
import hashlib
import json
import os
from email import policy
import re

# Load security rules from security_rules.json
SECURITY_RULES_PATH = os.path.join(os.path.dirname(__file__), "dataset", "security_rules.json")

def load_security_rules():
    """
    Load security rules from the JSON file.
    """
    if os.path.exists(SECURITY_RULES_PATH):
        with open(SECURITY_RULES_PATH, "r") as file:
            return json.load(file)
    return []

def encrypt_data(data):
    """
    Encrypt sensitive data by shifting each character by +2.
    For example, 'B' becomes 'D', '1' becomes '3'.
    """
    encrypted = []
    for char in data:
        if char.isalpha():  # If the character is a letter
            # Shift within the alphabet (preserve case)
            if char.islower():
                encrypted.append(chr((ord(char) - ord('a') + 2) % 26 + ord('a')))
            else:
                encrypted.append(chr((ord(char) - ord('A') + 2) % 26 + ord('A')))
        elif char.isdigit():  # If the character is a digit
            # Shift within the range of digits
            encrypted.append(chr((ord(char) - ord('0') + 2) % 10 + ord('0')))
        else:
            # Leave other characters unchanged
            encrypted.append(char)
    return ''.join(encrypted)

def apply_security_rules(email_content):
    """
    Apply security rules to classify_content and encrypt sensitive data.
    """
    security_rules = load_security_rules()

    # Extract rules from the JSON
    for rule in security_rules:
        collection = rule.get("collection", "Confidential")
        patterns = rule.get("rules", [])

        # Check for sensitive patterns in the subject, body, and attachments
        for pattern in patterns:
            # Use regex to find the pattern and the word/phrase following it until a newline
            matches = re.finditer(rf"{pattern}\s*(.*?)(?=\\n|$)", email_content["classify_content"], re.IGNORECASE)
            for match in matches:
                sensitive_data = match.group(0)  # Extract the matched text
                encrypted_data = encrypt_data(sensitive_data)  # Encrypt the sensitive data
                email_content["classify_content"] = email_content["classify_content"].replace(sensitive_data, encrypted_data)

                
    return email_content
