import json
import os
def classification_Prompt(mail_content,request_types):
    try:
        
        prompt = f"""
        You are a classification assistant. Analyze the following content and classify it into:
        - Content Primary Ask
        - Content Secondary Ask        
        - Key Elements (specific keywords, phrases, or data points)
        
        Additional Context:
        - The content may include multiple requests or actions. Focus on identifying the primary intent of the content and classify it accordingly.
        - Prioritize the following request types in case of conflicts:
            {load_prioritization_rules()}
        - Extract specific keywords, phrases, or data points such as dates, amounts, names, or references.
        - **Relevant Context**: If there is any other relevant information in the content (e.g., a funding request), mention how it fits into the classification.

        List all possible request types and subtypes. Based on the following possible request types and subtypes:
        {request_types}

        Content: "{mail_content}"

        Respond in the following JSON format:
        {{
            "PrimaryAsk": "<primary_ask>",
            "SecondaryAsk": "<secondary_ask>",            
            "KeyElements": [
                "<key_element_1>",
                "<key_element_2>",
                "<key_element_3>"
            ],
            "reasoning": "<reasoning: why the content was classified as high confidence_score even thuogh it has some other possible request types>"
            "Request": [
                {{
                    "request_type": "<type>",
                    "request_subtype": "<subtype>",
                    "confidence_score": <score>
                }},
                {{
                    "request_type": "<type>",
                    "request_subtype": "<subtype>",
                    "confidence_score": <score>                    
                }}
            ]
        }}
        """
  
        return prompt

    except Exception as e:
        return {"error": str(e)}

def generate_reasoning(content, chosen_type, chosen_subtype, request_types_list):
    """
    Generates reasoning for why a specific request type and subtype were chosen.
    :param content: The content being classified.
    :param chosen_type: The chosen request type.
    :param chosen_subtype: The chosen request subtype.
    :param request_types_list: The list of all possible request types and subtypes.
    :return: A detailed reasoning string.
    """
    reasoning = f"The chosen request type is '{chosen_type}' with subtype '{chosen_subtype}' because the content mentions "
    if chosen_subtype:
        reasoning += f"'{chosen_subtype}', which directly aligns with the content. "
    else:
        reasoning += f"'{chosen_type}', which is the most relevant category. "

    # Add reasoning for why other request types were not chosen
    reasoning += "Other request types were not chosen because they do not match the key elements in the content. For example, "
    for request_type in request_types_list:
        if request_type["type"] != chosen_type:
            reasoning += f"'{request_type['type']}' does not align with the content. "

    return 

def load_prioritization_rules():
    """
    Load prioritization rules from a JSON file and format them for the prompt.
    :param file_path: Path to the JSON file containing prioritization rules.
    :return: A formatted string of prioritization rules.
    """
    try:
        # Load the JSON file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        rule_path = os.path.abspath(os.path.join(current_dir, "dataset", "prioritization_rules.json"))
        
        with open(rule_path, "r") as file:
            rules_data = json.load(file)
        
        # Extract and format the rules
        rules = rules_data.get("PrioritizationRules", [])
        formatted_rules = "Prioritization Rules:\n"
        for rule in rules:
            formatted_rules += f"{rule['priority']}. {', '.join(rule['request_type'])}: {rule['description']}\n"
        print (formatted_rules.strip())
        return formatted_rules.strip()
    except Exception as e:
        return f"Error loading prioritization rules: {e}"

if __name__ == "__main__":
    load_prioritization_rules()