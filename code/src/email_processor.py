import email
import os
import json
import pytesseract
import pdfplumber
from PIL import Image, ImageEnhance
from docx import Document
from email import policy
from email.parser import BytesParser

def clean_text(text):
    """Remove unwanted special characters from text."""
    return text.replace("\ufeff", "").replace("\u00a0", " ").strip()

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file with better layout handling"""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text(layout=True) + "\n"
    except Exception as e:
        text = f"Could not extract text: {str(e)}"
    return clean_text(text)

def extract_text_from_docx(file_path):
    """Extract text from a Word document"""
    text = ""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        text = f"Could not extract text: {str(e)}"
    return clean_text(text)

def extract_text_from_image(file_path):
    """Extract text from an image using OCR with preprocessing"""
    try:
        image = Image.open(file_path).convert('L')  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Increase contrast
        return clean_text(pytesseract.image_to_string(image))
    except Exception as e:
        return f"Could not extract text: {str(e)}"

def save_attachment(part, save_path):
    """Save attachment from the email part and return its content in a readable format"""
    filename = part.get_filename()
    if filename:
        file_path = os.path.join(save_path, filename)
        content = part.get_payload(decode=True)
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        try:
            if part.get_content_type() in ["text/plain", "text/csv", "application/json"]:
                attachment_content = clean_text(content.decode('utf-8', errors='replace'))
            elif part.get_content_type() == "application/pdf":
                attachment_content = extract_text_from_pdf(file_path)
            elif part.get_content_type() in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                attachment_content = extract_text_from_docx(file_path)
            elif part.get_content_type().startswith("image/"):
                attachment_content = extract_text_from_image(file_path)
            else:
                attachment_content = "Unsupported file type"
        except Exception as e:
            attachment_content = f"Could not extract text: {str(e)}"
        
        return {
            "filename": filename,
            "path": file_path,
            "content_type": part.get_content_type(),
            "content": attachment_content
        }
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
                    body += clean_text(part.get_payload(decode=True).decode(part.get_content_charset(), errors='replace'))
                elif 'attachment' in content_disposition:
                    attachment_info = save_attachment(part, save_dir)
                    if attachment_info:
                        attachments.append(attachment_info)
        else:
            body = clean_text(msg.get_payload(decode=True).decode(msg.get_content_charset(), errors='replace'))
        
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