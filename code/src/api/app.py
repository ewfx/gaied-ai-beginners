import json
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from aimain import process_and_classify_emails
from requesttypes_app import router as requesttypes_router
from prioritizationrules_app import router as prioritizationrules_router
from securityrules_app import router as securityrules_router
import os

# Initialize FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define request body schema
class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"response": "Welcome to the Gen AI API!"}

    
@app.get("/process_and_classify_emails")
async def process_and_classify_emails_endpoint():
    try:
        response = process_and_classify_emails()       
        return {"response": response}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# API to get classified_mail.json
@app.get("/classified-mails")
async def get_classified_mails():
    file_path = os.path.join("data", "classified_mail.json")  # Adjust the path as needed
    CLASSIFIED_MAIL_JSON = os.path.join(
    os.path.dirname(__file__), "dataset", "db_data", "classified_mail.json"
    )
    if os.path.exists(CLASSIFIED_MAIL_JSON):
        with open(CLASSIFIED_MAIL_JSON, "r") as file:
            return json.load(file)
    return []

# API to get duplicate_mail.json
@app.get("/duplicate-mails")
async def get_duplicate_mails():
    file_path = os.path.join("data", "duplicate_mail.json")  # Adjust the path as needed
    DUPLICATE_MAIL_JSON = os.path.join(
    os.path.dirname(__file__), "dataset", "db_data", "duplicate_mail.json"
    )
    if os.path.exists(DUPLICATE_MAIL_JSON):
        with open(DUPLICATE_MAIL_JSON, "r") as file:
            duplicate_emails = json.load(file)
        return duplicate_emails


UPLOAD_FOLDER = "uploaded_files"  # Define the folder where files will be saved

# API to upload a file
@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), "..", "mail_dropbox", "unread"
    )

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"File '{file.filename}' uploaded successfully to '{UPLOAD_FOLDER}'."}

# Include the routers
app.include_router(requesttypes_router, prefix="/request-types", tags=["Request Types"])
app.include_router(prioritizationrules_router, prefix="/prioritization-rules", tags=["Prioritization Rules"])
app.include_router(securityrules_router, prefix="/security-rules", tags=["Security Rules"])
