from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json

# Define the router
router = APIRouter()

# Path to the JSON file
SECURITY_RULES_FILE = os.path.join("dataset", "security_rules.json")

# Define the Pydantic model for a security rule
class SecurityRule(BaseModel):
    collection: str
    rules: list[str]

# Helper function to load security rules from the JSON file
def load_security_rules():
    if not os.path.exists(SECURITY_RULES_FILE):
        return []
    with open(SECURITY_RULES_FILE, "r") as file:
        return json.load(file)

# Helper function to save security rules to the JSON file
def save_security_rules(rules):
    with open(SECURITY_RULES_FILE, "w") as file:
        json.dump(rules, file, indent=4)

# 1. Get all security rules
@router.get("/security-rules", response_model=list[SecurityRule])
async def get_security_rules():
    return load_security_rules()

# 2. Get a single security rule by collection name
@router.get("/security-rules/{collection_name}", response_model=SecurityRule)
async def get_security_rule(collection_name: str):
    rules = load_security_rules()
    for rule in rules:
        if rule["collection"].lower() == collection_name.lower():
            return rule
    raise HTTPException(status_code=404, detail="Security rule not found")

# 3. Create a new security rule
@router.post("/security-rules", response_model=SecurityRule)
async def create_security_rule(new_rule: SecurityRule):
    rules = load_security_rules()
    # Check for duplicate collection
    if any(r["collection"].lower() == new_rule.collection.lower() for r in rules):
        raise HTTPException(status_code=400, detail="Rule with this collection already exists")
    rules.append(new_rule.dict())
    save_security_rules(rules)
    return new_rule

# 4. Update an existing security rule by collection name
@router.put("/security-rules/{collection_name}", response_model=SecurityRule)
async def update_security_rule(collection_name: str, updated_rule: SecurityRule):
    rules = load_security_rules()
    for index, rule in enumerate(rules):
        if rule["collection"].lower() == collection_name.lower():
            rules[index] = updated_rule.dict()
            save_security_rules(rules)
            return updated_rule
    raise HTTPException(status_code=404, detail="Security rule not found")

# 5. Delete a security rule by collection name
@router.delete("/security-rules/{collection_name}")
async def delete_security_rule(collection_name: str):
    rules = load_security_rules()
    for index, rule in enumerate(rules):
        if rule["collection"].lower() == collection_name.lower():
            del rules[index]
            save_security_rules(rules)
            return {"message": "Security rule deleted successfully"}
    raise HTTPException(status_code=404, detail="Security rule not found")