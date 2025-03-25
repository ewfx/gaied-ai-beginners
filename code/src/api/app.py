from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aimain import process_and_classify_emails
from requesttypes_app import router as requesttypes_router
from prioritizationrules_app import router as prioritizationrules_router

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

# Include the routers
app.include_router(requesttypes_router, prefix="/request-types", tags=["Request Types"])
app.include_router(prioritizationrules_router, prefix="/prioritization-rules", tags=["Prioritization Rules"])
app.include_router(requesttypes_router, prefix="/request-types", tags=["Request Types"])
app.include_router(prioritizationrules_router, prefix="/unread-emails", tags=["Read Unread Emails"])