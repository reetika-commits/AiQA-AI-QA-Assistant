def agent_prompt_builder(page_text,relevant_dom, request):

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
    return f"""
    You are an experienced QA Automation Engineer.

    Generate comprehensive test cases for the following requirement.

    Requirement:
    {request}

    The following information was collected from the live application.

    VISIBLE PAGE TEXT:
    {page_text}

    DOM:
    {relevant_dom}

    Use the page text and DOM to understand the actual UI elements,
    fields, buttons, links and available functionality.

    Return ONLY valid JSON.

    The root object MUST contain a key named "testcases".

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
    6. Do not include markdown, comments, or explanations.
    """