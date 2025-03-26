import datetime
import email
import os
import json
from email import policy
from email.parser import BytesParser
import extract_msg
import mimetypes
from secure_app import apply_security_rules
from doc_processor import read_document

def read_eml_file(file_path):
    """
    Reads an .eml file and extracts its content.
    """
    with open(file_path, "rb") as file:
        msg = BytesParser(policy=policy.default).parse(file)

        email_content = {
            "message_id": msg["Message-ID"], 
            "in_reply_to": msg["In-Reply-To"],
            "references": msg["References"],
            "subject": msg["subject"],
            "from": msg["from"],
            "to": msg["to"],
            "date": msg["date"],
            "body": msg.get_body(preferencelist=("plain", "html")).get_content() if msg.get_body() else "",
            "attachments": []
        }
        
        # Extract attachments
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                # Get the file extension
                _, file_extension = os.path.splitext(filename)

                # Read the content of the attachment
                attachment_content = part.get_content()

                # Process the attachment content if it's a supported file type
                try:
                    extracted_content = read_document(attachment_content, file_extension)
                except ValueError as e:
                    extracted_content = f"Error processing attachment: {e}"

                # Add attachment details to the email content
                attachment = {
                    "filename": filename,
                    "content_type": part.get_content_type(),
                    "size": len(attachment_content),
                    "file_extension": file_extension,
                    "content": extracted_content
                }
                email_content["attachments"].append(attachment)
        email_content["classify_content"] = json.dumps({
            "subject": email_content["subject"],
            "body": email_content["body"],
            "attachments": email_content["attachments"]
        })

        return email_content


def read_msg_file(file_path):
    """
    Reads a .msg file and extracts its content.
    """
    msg = extract_msg.Message(file_path)  # Open the .msg file
    try:
        email_content = {
            "message_id": msg.headers.get("Message-ID"),  # Extract the unique Message-ID
            "in_reply_to": msg["In-Reply-To"],  # Message-ID of the email this is replying to
            "references": msg["References"],
            "subject": msg.subject,
            "from": msg.sender,
            "to": msg.to,
            "date": msg.date.isoformat() if isinstance(msg.date, datetime.datetime) else msg.date,  # Convert datetime to string
            "body": msg.body if msg.body else msg.htmlBody,
            "attachments": []
        }
        
        # Extract attachments
        for attachment in msg.attachments:
            attachment_info = {
                "filename": attachment.longFilename or attachment.shortFilename,
                "size": len(attachment.data),
                "content": attachment.data
            }
            filename = attachment_info["filename"]
            if filename:
                # Get the file extension
                _, file_extension = os.path.splitext(filename)

                # Read the content of the attachment
                attachment_content = attachment_info["content"]
                content_type, _ = mimetypes.guess_type(filename)

                # Process the attachment content if it's a supported file type
                try:
                    extracted_content = read_document(attachment_content, file_extension)
                except ValueError as e:
                    extracted_content = f"Error processing attachment: {e}"

                # Add attachment details to the email content
                attachment = {
                    "filename": filename,
                    "content_type": content_type,
                    "size": len(attachment_content),
                    "file_extension": file_extension,
                    "content": extracted_content
                }
                email_content["attachments"].append(attachment)
        
        email_content["classify_content"] = json.dumps({
            "subject": email_content["subject"],
            "body": email_content["body"].decode() if isinstance(email_content["body"], bytes) else email_content["body"],
            "attachments": email_content["attachments"]
        })

        return email_content
    finally:
        # Ensure the .msg file is closed
        msg.close()

def convert_email_to_json(file_path):
    """
    Converts an email file (.eml or .msg) to JSON format.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".eml":
        email_content = read_eml_file(file_path)
    elif file_extension.lower() == ".msg":
        email_content = read_msg_file(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .eml or .msg file.")
    email_content = apply_security_rules(email_content)
    return email_content


# Example usage
if __name__ == "__main__":
    file_path = "ABC Bank share adjustment.eml"  
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        email_path = os.path.abspath(os.path.join(current_dir, "..", "mail_dropbox", "unread", file_path))
        email_json = convert_email_to_json(email_path)
        print("Email Content in JSON Format:")
        print(email_json)
    except Exception as e:
        print(f"Error: {e}")