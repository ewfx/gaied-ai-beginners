import hashlib
import json
import os
from difflib import SequenceMatcher
from utils import get_classify


# Filepath to the classified_mail.json
CLASSIFIED_MAIL_JSON = os.path.join(
    os.path.dirname(__file__), "dataset", "db_data", "classified_mail.json"
)

# Filepath to the duplicate_mail.json
DUPLICATE_MAIL_JSON = os.path.join(
    os.path.dirname(__file__), "dataset", "db_data", "duplicate_mail.json"
)

def load_processed_emails():
    """
    Load processed emails from classified_mail.json.
    """
    if os.path.exists(CLASSIFIED_MAIL_JSON):
        with open(CLASSIFIED_MAIL_JSON, "r") as file:
            return json.load(file)
    return []

def log_duplicate_email(email_content, reason):
    """
    Log duplicate email details to duplicate_mail.json with the reason and a unique record#.
    """
    duplicate_emails = []
    if os.path.exists(DUPLICATE_MAIL_JSON):
        with open(DUPLICATE_MAIL_JSON, "r") as file:
            duplicate_emails = json.load(file)

    # Determine the next record number
    next_record_number = 1
    if duplicate_emails:
        next_record_number = max(entry.get("record#", 0) for entry in duplicate_emails) + 1

    # Add the duplicate email with the reason and record#
    duplicate_emails.append({
        "record#": next_record_number,
        "message_id": email_content.get("message_id"),
        "subject": email_content.get("subject"),
        "from": email_content.get("from"),
        "to": email_content.get("to"),
        "date": email_content.get("date"),
        "reason": reason
    })

    # Write back to duplicate_mail.json
    with open(DUPLICATE_MAIL_JSON, "w") as file:
        json.dump(duplicate_emails, file, indent=4) 

def is_duplicate(email_content):
    """
    Check if the given email is a duplicate based on classified_mail.json.
    """
    processed_emails = load_processed_emails()

    # Check Message-ID
    for processed_email in processed_emails:
        if email_content["message_id"] == processed_email.get("message_id"):
            print("Duplicate email detected based on Message-ID.")
            log_duplicate_email(email_content, "Duplicate based on Message-ID.")
            return True
    
        # Check Reference-ID
    for processed_email in processed_emails:
        if email_content["references"] == processed_email.get("message_id"):
            print("Duplicate email detected based on references.")
            log_duplicate_email(email_content, f"Duplicate based on references. Might be follow-up mail for subject [{processed_email.get("subject")}].")
            return True

    for processed_email in processed_emails:
        request1 = email_content["classify_content"]
        request2 = processed_email.get("classify_content")
        prompt = f"""
            You are given two requests. Analyze their content and return a JSON response with the following format:
            {{
              "score": float,
              "reason": string
            }}
            Where:
            - "score" is a float between 0.0 and 100.0 that indicates how similar the requests are.
            - "reason" is a string explanation of why the two requests are semantically the same or different.
            New Mail: "{request1}"
            Old Mail: "{request2}"
            """
        data = get_classify(prompt)
        print(data)
        if data["score"] > 90:
            print("High-confidence duplicate email detected based on content.")
            log_duplicate_email(email_content, f"High-confidence duplicate based on content score {data['score']}. Reason: {data['reason']} ")
            return True
        elif 70 <= data["score"] <= 90:
            print("Medium-confidence duplicate email detected based on content.")
            log_duplicate_email(email_content, f"Medium-confidence duplicate based on content score {data['score']}. Reason: {data['reason']}")
            return True

    # Check Body Hash
    body_hash = hashlib.md5(email_content["body"].encode("utf-8")).hexdigest()
    for processed_email in processed_emails:
        processed_body_hash = hashlib.md5(
            processed_email["body"].encode("utf-8")
        ).hexdigest()
        if body_hash == processed_body_hash:
            print("Duplicate email detected based on body content.")
            log_duplicate_email(email_content, "Duplicate based on body content.")
            return True

    # Check Attachments
    for processed_email in processed_emails:
        for attachment in email_content["attachments"]:
            attachment_hash = hashlib.md5(
                attachment["content"].encode("utf-8")
            ).hexdigest()
            for processed_attachment in processed_email["attachments"]:
                processed_attachment_hash = hashlib.md5(
                    processed_attachment["content"].encode("utf-8")
                ).hexdigest()
                if attachment_hash == processed_attachment_hash:
                    print("Duplicate email detected based on attachments.")
                    log_duplicate_email(email_content, "Duplicate based on attachments.")
                    return True

    # Check Threading Information
    for processed_email in processed_emails:
        if (
            email_content["in_reply_to"] == processed_email.get("in_reply_to")
            and email_content["references"] == processed_email.get("references")
        ):
            print("Duplicate email detected based on threading information.")
            log_duplicate_email(email_content, "Duplicate based on threading information.")
            return True

    # If no duplicates are found
    return False
