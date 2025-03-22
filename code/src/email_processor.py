import os
import email
from email.parser import BytesParser
from email.header import decode_header
import PyPDF2
from docx import Document
from PIL import Image
from openapi_core import OpenAPIRequest

# Folder containing email files
EMAIL_FOLDER = 'E:\Hackthon 2025\gaied-ai-beginners\code\src\Emails'

# Loop through email files
for filename in os.listdir(EMAIL_FOLDER):
    if filename.endswith('.eml') or filename.endswith('.msg'):
        file_path = os.path.join(EMAIL_FOLDER, filename)

        # Parse email message
        with open(file_path, 'rb') as file:
            message = BytesParser().parsebytes(file.read())

        # Extract email subject and body
        subject = decode_header(message['Subject'])[0][0]
        body = ''
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
        
        # Extract attachments
        attachments = []
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename:
                attachments.append(filename)
        
        # Read attachment contents
        attachment_contents = []
        for attachment in attachments:
            if attachment.endswith('.pdf'):
                pdf_file = open(attachment, 'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                num_pages = pdf_reader.numPages
                for page in range(num_pages):
                    page_obj = pdf_reader.getPage(page)
                    attachment_contents.append(page_obj.extractText())
            elif attachment.endswith('.docx'):
                doc = Document(attachment)
                for para in doc.paragraphs:
                    attachment_contents.append(para.text)
            elif attachment.endswith(('.jpg', '.png', '.gif')):
                img = Image.open(attachment)
                attachment_contents.append(img.size)

        # Create OpenAPI request
        openapi_request = OpenAPIRequest(
            method='POST',
            path='/requests',
            body={
                'subject': subject,
                'body': body,
                'attachments': attachments,
                'attachment_contents': attachment_contents
            }
        )

        # Determine request type and sub-request type
        request_types = ['request_type_1', 'request_type_2', 'request_type_3']
        sub_request_types = ['sub_request_type_1', 'sub_request_type_2', 'sub_request_type_3']
        request_type_probabilities = [0.4, 0.3, 0.3]
        sub_request_type_probabilities = [0.6, 0.2, 0.2]

        # Print request type and sub-request type with probabilities
        print('Request Type:')
        for i, request_type in enumerate(request_types):
            print(f'{request_type}: {request_type_probabilities[i] * 100}%')
        print('Sub-RequestType:')
        for i, sub_request_type in enumerate(sub_request_types):
            print(f'{sub_request_type}: {sub_request_type_probabilities[i] * 100}%')
