from fastapi import FastAPI, HTTPException
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
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="classified_mail.json not found")
    return FileResponse(file_path, media_type="application/json", filename="classified_mail.json")

# API to get duplicate_mail.json
@app.get("/duplicate-mails")
async def get_duplicate_mails():
    file_path = os.path.join("data", "duplicate_mail.json")  # Adjust the path as needed
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="duplicate_mail.json not found")
    return FileResponse(file_path, media_type="application/json", filename="duplicate_mail.json")


# Include the routers
app.include_router(requesttypes_router, prefix="/request-types", tags=["Request Types"])
app.include_router(prioritizationrules_router, prefix="/prioritization-rules", tags=["Prioritization Rules"])
app.include_router(securityrules_router, prefix="/security-rules", tags=["Security Rules"])
