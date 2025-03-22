import email
import os
import json
from email import policy
from email.parser import BytesParser

def save_attachment(part, save_path):
    """Save attachment from the email part and return its content"""
    filename = part.get_filename()
    if filename:
        file_path = os.path.join(save_path, filename)
        with open(file_path, 'wb') as f:
            content = part.get_payload(decode=True)
            f.write(content)
        return {"filename": filename, "path": file_path, "content_type": part.get_content_type(), "content": content.hex()}
    return None

def process_email_content(subject, body, attachments):
    """Process email content and classify request type"""
    request_types = {"Technical Issue": ["error", "bug", "issue"],
                     "Billing": ["invoice", "payment", "refund"]}
    
    match_scores = {}
    
    for req_type, keywords in request_types.items():
        match_count = sum(1 for word in keywords if word in body.lower() or word in subject.lower())
        match_scores[req_type] = (match_count / len(keywords)) * 100  # Percentage match
    
    best_match = max(match_scores, key=match_scores.get)
    
    return {
        "request_type": best_match,
        "match_percentage": match_scores[best_match]
    }

def read_email_with_attachments(file_path, save_dir):
    """Read an email file and process its content, returning JSON output"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    with open(file_path, 'rb') as file:
        msg = BytesParser(policy=policy.default).parse(file)
        
        subject = msg['subject']
        from_email = msg['from']
        to_email = msg['to']
        date = msg['date']
        
        body = ""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                
                if content_type in ['text/plain', 'text/html']:
                    body += part.get_payload(decode=True).decode(part.get_content_charset(), errors='ignore')
                elif 'attachment' in content_disposition:
                    attachment_info = save_attachment(part, save_dir)
                    if attachment_info:
                        attachments.append(attachment_info)
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset())
        
        classification = process_email_content(subject, body, attachments)
        
        email_data = {
            "subject": subject,
            "from": from_email,
            "to": to_email,
            "date": date,
            "body": body,
            "attachments": attachments,
            "classification": classification
        }
        
        output_path = os.path.join(save_dir, "email_output.json")
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(email_data, json_file, indent=4)
        
        return email_data

def process_emails_in_folder(email_folder, output_folder):
    """Process all .eml files in a folder and save JSON output"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(email_folder):
        if filename.endswith('.eml'):
            email_file_path = os.path.join(email_folder, filename)
            email_output_dir = os.path.join(output_folder, filename.replace('.eml', ''))
            if not os.path.exists(email_output_dir):
                os.makedirs(email_output_dir)
            
            email_data = read_email_with_attachments(email_file_path, email_output_dir)
            json_output_path = os.path.join(email_output_dir, f"{filename.replace('.eml', '.json')}")
            with open(json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(email_data, json_file, indent=4)
            print(json.dumps(email_data, indent=4))

# Example usage
email_folder = 'E:\\Hackthon 2025\\gaied-ai-beginners\\code\\src\\Emails'
output_folder = 'emails_output'

process_emails_in_folder(email_folder, output_folder)