from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
import json
import os

router = APIRouter()

# Filepath for the prioritization rules JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
PRIORITIZATION_RULES_FILE = os.path.abspath(os.path.join(current_dir, "dataset", "prioritization_rules.json"))

# Pydantic model for a single prioritization rule
class PrioritizationRule(BaseModel):
    priority: int
    request_type: List[str]
    description: str

class UpdatePrioritizationRule(BaseModel):
    request_type: Optional[List[str]] = None
    description: Optional[str] = None

# Endpoint to get all prioritization rules
@router.get("/prioritization-rules")
def get_prioritization_rules():
    """
    Get all prioritization rules from the JSON file.
    """
    try:
        with open(PRIORITIZATION_RULES_FILE, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading prioritization rules: {e}")

# Endpoint to insert a new prioritization rule
@router.post("/prioritization-rules")
def insert_prioritization_rule(rule: PrioritizationRule):
    """
    Insert a new prioritization rule into the JSON file.
    """
    try:
        with open(PRIORITIZATION_RULES_FILE, "r") as file:
            data = json.load(file)

        # Check if the priority already exists
        for existing_rule in data["PrioritizationRules"]:
            if existing_rule["priority"] == rule.priority:
                raise HTTPException(status_code=400, detail="A rule with this priority already exists.")

        # Add the new rule
        data["PrioritizationRules"].append(rule.dict())

        # Sort the rules by priority
        data["PrioritizationRules"] = sorted(data["PrioritizationRules"], key=lambda x: x["priority"])

        # Write back to the file
        with open(PRIORITIZATION_RULES_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "Prioritization rule added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting prioritization rule: {e}")

# Endpoint to update an existing prioritization rule
@router.put("/prioritization-rules/{priority}")
def update_prioritization_rule(priority: int, update_data: UpdatePrioritizationRule):
    """
    Update an existing prioritization rule in the JSON file.
    """
    try:
        with open(PRIORITIZATION_RULES_FILE, "r") as file:
            data = json.load(file)

        # Find the rule to update
        for rule in data["PrioritizationRules"]:
            if rule["priority"] == priority:
                if update_data.request_type is not None:
                    rule["request_type"] = update_data.request_type
                if update_data.description is not None:
                    rule["description"] = update_data.description
                break
        else:
            raise HTTPException(status_code=404, detail="Prioritization rule not found.")

        # Write back to the file
        with open(PRIORITIZATION_RULES_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "Prioritization rule updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating prioritization rule: {e}")

# Endpoint to delete a prioritization rule
@router.delete("/prioritization-rules/{priority}")
def delete_prioritization_rule(priority: int):
    """
    Delete a prioritization rule from the JSON file.
    """
    try:
        with open(PRIORITIZATION_RULES_FILE, "r") as file:
            data = json.load(file)

        # Find and remove the rule
        for i, rule in enumerate(data["PrioritizationRules"]):
            if rule["priority"] == priority:
                del data["PrioritizationRules"][i]
                break
        else:
            raise HTTPException(status_code=404, detail="Prioritization rule not found.")

        # Write back to the file
        with open(PRIORITIZATION_RULES_FILE, "w") as file:
            json.dump(data, file, indent=4)

        return {"message": "Prioritization rule deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting prioritization rule: {e}")