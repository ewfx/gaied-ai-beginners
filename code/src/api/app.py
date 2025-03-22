from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from aimain import get_classify,classify_content

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
    model: str = "gpt-4o-mini"

@app.get("/")
def root():
    return {"response": "Welcome to the Gen AI API!"}

@app.post("/classify/")
async def chat_completion(request: ChatRequest):
    try:
        response = get_classify(prompt=request.prompt, model=request.model)
        return {"response": response}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/classify-content/{prompt}")
async def classify_content_endpoint(prompt: str, model: str = "gpt-4o-mini"):
    try:
        prompt = "I need help with my loan application status."
        response = classify_content(prompt=prompt, model=model)
        return {"response": response}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
