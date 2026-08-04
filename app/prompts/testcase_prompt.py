import json

def create_prompt(requirements):
    print("Inside Prompt builder",flush=True)
    return prompt_builder(get_requirements(requirements))
    

def prompt_builder(request):

    json_template = """
    {
    "testcases": [
        {
            "title": "",
            "preconditions": "",
            "test_steps": "",
            "expected_result": "",
            "priority": ""
        }
    ]
    }
    """
    return f"""You are an experienced QA Automation Engineer.
        Generate comprehensive test cases for the following requirement.
        Requirement:{request}
        Return ONLY valid JSON.
        The root object MUST contain a key named "testcases".
        Do NOT return a single testcase object.
        The response MUST exactly follow this schema:
        {json_template}
        Rules:
        1. Generate one JSON object for each test case.
        2. Every test case must contain:
        - title
        - preconditions
        - test_steps
        - expected_result
        - priority
        3. Do not omit any field.
        4. If a value is not applicable, use an empty string ("").
        5. Return only the JSON object.
        6. Do not include markdown (```), comments, or explanations.
        Generate one object for EACH test case.
        Every object MUST contain ALL five fields.
        Do not omit any field.
        If a value is unknown, return an empty string.
        Do not return markdown or explanations.
        """
def get_requirements(requirements):
    with open(f"app/sample_data/{requirements}.json","r") as requirements_file:
        return json.load(requirements_file)