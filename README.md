# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A brief overview of your project and its purpose. Mention which problem statement are your attempting to solve. Keep it concise and engaging.

Project Overview:

Our project focuses on developing a Generative AI-powered email classification and OCR solution that can accurately extract, interpret context, and categorize emails with high precision. The primary goal is to enhance email management by automating the sorting, prioritization, and contextual understanding of incoming messages.

Problem Statement:

Businesses and individuals often face challenges in managing high volumes of emails, leading to inefficiencies, missed opportunities, and increased workload. Traditional email filtering systems rely on keyword-based or rule-based classification, which often lacks adaptability to nuanced contexts.

Solution:

Our AI-driven system integrates natural language processing (NLP), optical character recognition (OCR), and deep learning to:

Extract key information from email content and attachments.

Understand the intent and context using advanced language models.

Classify emails into relevant categories automatically.

Prioritize emails based on urgency, sender importance, or predefined criteria.

This solution aims to streamline workflows, reduce manual effort, and improve decision-making by providing smart, context-aware email management for organizations and professionals.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
What inspired you to create this project? Describe the problem you're solving.

The idea for this project was inspired by the increasing need for smarter email management in today’s fast-paced digital world. Many organizations struggle with email overload, making it difficult to keep track of important communications and prioritize responses effectively. Manual sorting and rule-based filters often fail to adapt to evolving business needs and unstructured content within emails and attachments. By leveraging AI-driven automation, we aim to redefine email organization and ensure that users can focus on high-priority tasks. 

Managing emails manually can be time-consuming, especially for organizations dealing with a high volume of messages. Existing rule-based filters often fall short when handling unstructured email content, attachments, and context-based prioritization. As businesses grow, the need for a more efficient, AI-driven email classification system becomes critical. Our goal is to build a solution that automates email categorization, understands context, and helps users focus on important tasks without being buried under an overwhelming inbox.

## ⚙️ What It Does
Explain the key features and functionalities of your project.

Here’s a detailed explanation of the key features and functionalities of your email processing solution:

Key Features and Functionalities:
1. AI-Powered Email Classification
   - Uses Gen AI to analyze and categorize emails based on their subject and content includes attachements.
   - Identifies common request types such as Adjustment, AU Transfer, Closing Notice etc using keyword-based matching.

2. OCR (Optical Character Recognition) for Attachments
   - Extracts text from PDF, DOCX, and image files attached to emails.
   - Uses pytesseract for OCR-based text extraction from images.
   - Enhances images for better OCR accuracy by increasing contrast and converting them to grayscale.

3. Multi-Format Email Attachment Processing
   - Supports multiple file types, including:
      - Text-based files (TXT, CSV, JSON)
      - Document files (DOCX, PDF)
      - Images (JPG, PNG)
   - Extracts and stores the extracted text for further analysis.

4. Email Parsing and Metadata Extraction
   - Reads emails from .eml files.
   - Extracts critical metadata such as:
       - Sender, Recipient, Subject, and Date.
   - Processes both plain text and HTML email bodies.

5. Intelligent Content Classification
   - Analyzes the subject line and email body to determine the category of the request.
   - Uses a keyword-based matching algorithm to assign a percentage match to each request type.

6. Automated Email Processing
   - Scans an entire folder of emails (.eml files).
   - Saves extracted data and classification results as structured JSON files.
   - Enables bulk email processing for enterprise use cases.

7. Secure Attachment Handling
   - Saves attachments securely in a specified directory.
   - Ensures unsupported file types are not processed.

This system is designed to automate email processing, improve efficiency in handling customer queries, and enable businesses to respond faster to critical requests.

## 🛠️ How We Built It
Briefly outline the technologies, frameworks, and tools used in development.

**Technologies & Tools Used**
**1.	**Programming Language****
    - **Python** – Core development language for email processing, text extraction, and classification.
**2.	**Email Processing****
    -	**email.policy, email.parser** – To parse and process email content and attachments.
**3.	**Text Extraction & OCR****
    - **pdfplumber** – Extracts text from PDFs with structured layout handling.
    - **python-docx** – Reads and extracts content from Word documents (.docx).
    - **pytesseract** – Optical Character Recognition (OCR) for extracting text from images.
    - **Pillow (PIL)** – Image preprocessing (grayscale conversion, contrast enhancement).
**4.	**Data Handling & Storage****
    - **json** – Stores extracted email content in structured format.
    - **os** – Manages file system operations (saving attachments, creating directories).
**5.**	Classification & NLP Techniques****
    - **Regex & String Matching** – Identifies keywords for email classification.
    - **TF-IDF (Future Enhancement)** – Improves classification accuracy with better text understanding.
**6.	Execution & Environment Management**
    - **Virtual Environments (venv)** – Ensures dependency consistency across different setups.
    - **Requirements.txt** – Manages dependencies for easy deployment.

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

Technical Challenges & Solutions
1. Extracting Text from Various Attachments
   -	Issue: Different file formats (PDF, DOCX, images) require different extraction methods.
   -	Solution:
        -	Used pdfplumber for structured PDFs and python-docx for Word files.
        -	Applied OCR (pytesseract) with image preprocessing (grayscale + contrast) for scanned documents.
2. Handling Unstructured Email Content
   -	Issue: Emails contain a mix of HTML, plain text, and inline elements, making extraction tricky.
   -	Solution:
        -	Parsed email parts using email.policy.default.
        -	Converted HTML to text while filtering out signatures and disclaimers with regex.
3. Improving Email Classification Accuracy
   -	Issue: Simple keyword matching led to incorrect classification.
   -	Solution:
        -	Used TF-IDF scoring to weigh keywords more effectively.
        -	Future enhancement: NLP-based AI model for contextual understanding.
4. Processing Large Volumes Efficiently
   -	Issue: High email volume caused slow processing due to I/O bottlenecks.
   -	Solution:
        -	Implemented batch processing and asynchronous file handling.
        -	Streamed large attachments instead of loading them into memory.
________________________________________
Non-Technical Challenges
1. Data Privacy & Security
   -	Issue: Handling confidential data in emails and attachments.
   -	Solution: Implemented encryption and secure storage following compliance standards.
2. Managing Dependencies & Environment Consistency
   -	Issue: Conflicting library versions across different setups.
   -	Solution: Used virtual environments (venv) and standardized dependencies with requirements.txt.
3. Handling Email Format Variability
   -	Issue: Different email clients format emails inconsistently.
   -	Solution: Collected diverse samples and implemented fallback parsing methods.



## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React / Vue / Angular
- 🔹 Backend: Node.js / FastAPI / Django
- 🔹 Database: PostgreSQL / Firebase
- 🔹 Other: OpenAI API / Twilio / Stripe

## 👥 Team
- **Kannan K**      - [GitHub](https://github.com/uk2nk) | [LinkedIn](https://www.linkedin.com/in/kannan-krishnan-a7693b61/)
- **Udhayakumar G** - [GitHub](https://github.com/udhayakumar-g) | [LinkedIn](https://www.linkedin.com/in/udhaya-kumar-dot-net-dev/)
- **Manimaran M**   - [GitHub] | [LinkedIn]
- **Yogesh H**      - [GitHub] | [LinkedIn]
