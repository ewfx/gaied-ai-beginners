import os
from fastapi import  HTTPException,APIRouter
from pydantic import BaseModel
import json
from typing import List, Optional

router = APIRouter()

# Filepath for the JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
REQUEST_TYPES_FILE = os.path.abspath(os.path.join(current_dir, "dataset", "request-type.json"))

# Pydantic model for request types
class SubRequestType(BaseModel):
    subRequestTypes: List[str]

class RequestType(BaseModel):
    type: str
    subRequestTypes: List[str]

class UpdateRequestType(BaseModel):
    type: str
    subRequestTypes: Optional[List[str]] = None

# Endpoint to read all request types
@router.get("/request-types")
def read_request_types():
    """
    Read all request types from the JSON file.
    """
    try:
        with open(REQUEST_TYPES_FILE, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading request types: {e}")

# Endpoint to add a new request type
@router.post("/request-types")
def add_request_type(request_type: RequestType):
    """
    Add a new request type to the JSON file.
    """
    try:
        with open(REQUEST_TYPES_FILE, "r") as file:
            data = json.load(file)

        # Check if the request type already exists
        for existing_type in data["CommercialBankLendingService"]["RequestTypes"]:
            if existing_type["type"] == request_type.type:
                raise HTTPException(status_code=400, detail="Request type already exists.")

        # Add the new request type
        data["CommercialBankLendingService"]["RequestTypes"].append(request_type.dict())

        # Write back to the file
        with open(REQUEST_TYPES_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "Request type added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding request type: {e}")

# Endpoint to update an existing request type
@router.put("/request-types/{request_type_name}")
def update_request_type(request_type_name: str, update_data: UpdateRequestType):
    """
    Update an existing request type in the JSON file.
    """
    try:
        with open(REQUEST_TYPES_FILE, "r") as file:
            data = json.load(file)

        # Find the request type to update
        for existing_type in data["CommercialBankLendingService"]["RequestTypes"]:
            if existing_type["type"] == request_type_name:
                if update_data.subRequestTypes:
                    existing_type["subRequestTypes"] = update_data.subRequestTypes
                break
        else:
            raise HTTPException(status_code=404, detail="Request type not found.")

        # Write back to the file
        with open(REQUEST_TYPES_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "Request type updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating request type: {e}")

# Endpoint to delete a request type
@router.delete("/request-types/{request_type_name}")
def delete_request_type(request_type_name: str):
    """
    Delete a request type from the JSON file.
    """
    try:
        with open(REQUEST_TYPES_FILE, "r") as file:
            data = json.load(file)

        # Find and remove the request type
        for i, existing_type in enumerate(data["CommercialBankLendingService"]["RequestTypes"]):
            if existing_type["type"] == request_type_name:
                del data["CommercialBankLendingService"]["RequestTypes"][i]
                break
        else:
            raise HTTPException(status_code=404, detail="Request type not found.")

        # Write back to the file
        with open(REQUEST_TYPES_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "Request type deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting request type: {e}")