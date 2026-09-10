def vision_prompt_builder(request, relevant_dom, retrieved_testcases):
    return f"""
    You are an experienced QA Automation Engineer.

    Generate test cases for the CURRENT REQUIREMENT using the UI elements
    identified by the Vision analysis and the retrieved historical test cases.

    CURRENT REQUIREMENT:
    {request}

    RELEVANT DOM ELEMENTS IDENTIFIED BY VISION:
    {relevant_dom}

    RETRIEVED HISTORICAL TEST CASES:
    {retrieved_testcases}

    IMPORTANT RULES:

    1. The CURRENT REQUIREMENT is the primary source of truth for what
    needs to be tested.

    2. The RELEVANT DOM ELEMENTS IDENTIFIED BY VISION represent the UI
    elements relevant to the feature currently being analyzed.

    3. RETRIEVED HISTORICAL TEST CASES are reference material only.
    They may have been created for a different application.

    4. Use historical test cases to identify useful TESTING INTENT,
    COVERAGE, and applicable negative or positive scenarios.

    5. Adapt the testing intent from historical test cases to the
    CURRENT REQUIREMENT and the RELEVANT DOM ELEMENTS.

    6. EVERY UI element mentioned in test_steps MUST be supported by the
    RELEVANT DOM ELEMENTS IDENTIFIED BY VISION.

    7. Do not assume that a UI element exists merely because it appears
    in a historical test case.

    8. If a historical test case contains a UI element that is not present
    in the RELEVANT DOM ELEMENTS, do not use that element or any step
    that depends on it.

    9. If a historical test case uses a different label, field name,
    button name, or other UI identifier, use the identifier provided
    by the RELEVANT DOM ELEMENTS.

    10. Do not introduce credentials from historical test cases.
        Credentials may only be used when explicitly provided by the
        CURRENT REQUIREMENT or clearly supported by the RELEVANT DOM
        ELEMENTS.

    11. Do not introduce workflows, pages, UI behavior, or application-
        specific behavior from historical test cases unless supported by
        the CURRENT REQUIREMENT or RELEVANT DOM ELEMENTS.

    12. Retrieved expected results are reference material only. Generate
        expected results based on the CURRENT REQUIREMENT and behavior
        supported by the available UI information.

    13. If information from historical test cases conflicts with the
        CURRENT REQUIREMENT or RELEVANT DOM ELEMENTS, ignore the
        conflicting historical information.

    14. Do not invent application-specific details.

    15. Do not create duplicate test cases unnecessarily.

    16. If the retrieved historical test cases do not provide adequate
        coverage, create additional test cases based on the CURRENT
        REQUIREMENT and RELEVANT DOM ELEMENTS.

    17. Do not mention uncertainty using phrases such as "if applicable",
        "if available", or "if present". Only include test steps supported
        by the current requirement or relevant DOM.

    Before returning the answer, perform a final validation:

    - Every UI element in every test step is supported by the RELEVANT DOM.
    - Every credential used is supported by the CURRENT REQUIREMENT or
    relevant DOM.
    - No historical-only UI element or behavior has been introduced.
    - Test cases are relevant to the CURRENT REQUIREMENT.
    - Duplicate test cases are avoided.

    Return valid JSON only.

    The response MUST follow this structure:

    {{
        "testcases": [
            {{
                "title": "",
                "preconditions": "",
                "test_steps": "",
                "expected_result": "",
                "priority": ""
            }}
        ]
    }}

    Do not include explanations, comments, or markdown outside the JSON.
    """

def rag_prompt_builder(request, relevant_dom, retrieved_testcases):
    return f"""
    You are an experienced QA Automation Engineer.

    Your task is to generate test cases for the CURRENT REQUIREMENT.

    CURRENT REQUIREMENT:
    {request}

    ==================================================
    CURRENT APPLICATION UI - SOURCE OF TRUTH
    ==================================================

    The following DOM was extracted from the CURRENT LIVE APPLICATION.

    {relevant_dom}

    IMPORTANT:
    This is the authoritative source for the current application's UI.

    ==================================================
    HISTORICAL TEST CASES - REFERENCE ONLY
    ==================================================

    The following test cases were retrieved from previous applications.
    They are provided only to suggest testing ideas and improve coverage.

    {retrieved_testcases}

    ==================================================
    GENERATION RULES
    ==================================================

    1. The CURRENT REQUIREMENT defines WHAT must be tested.

    2. The CURRENT APPLICATION UI defines WHICH UI elements currently
    exist and how they are identified.

    3. Historical test cases are REFERENCE MATERIAL ONLY.
    They may belong to a different application.

    4. NEVER copy a historical test case directly.

    5. First determine the scenario required by the CURRENT REQUIREMENT.

    6. Then identify the UI elements needed for that scenario from the
    CURRENT APPLICATION UI.

    7. Use historical test cases only AFTER understanding the current
    requirement and current UI.

    8. Every UI element mentioned in test_steps MUST exist in the
    CURRENT APPLICATION UI.

    9. Use the CURRENT application's labels, values, buttons, fields,
    controls, and options. Never inherit these from historical cases.

    10. Do NOT inherit from historical test cases:
        - number of UI elements
        - labels
        - field names
        - button names
        - default states
        - page names
        - credentials
        - values
        - workflows
        - application-specific behavior

    11. If historical information conflicts with the CURRENT REQUIREMENT
        or CURRENT APPLICATION UI, IGNORE the historical information.

    12. Do not invent application-specific details that are not supported
        by the CURRENT REQUIREMENT or CURRENT APPLICATION UI.

    13. Historical expected results are reference material only.
        Generate expected results appropriate for the CURRENT APPLICATION.

    14. If historical test cases do not adequately cover the requirement,
        create appropriate test cases using the CURRENT REQUIREMENT and
        CURRENT APPLICATION UI.

    15. Do not create unnecessary duplicate test cases.

    ==================================================
    FINAL VALIDATION
    ==================================================

    Before returning each test case, verify:

    - It tests the CURRENT REQUIREMENT.
    - Every UI element in test_steps exists in the CURRENT APPLICATION UI.
    - Every UI label comes from the CURRENT APPLICATION UI.
    - No historical application-specific detail was copied.
    - The test case makes sense for the CURRENT APPLICATION.
    - The test case could NOT have been generated correctly using the
    historical test case alone.

    If any validation fails, rewrite the test case using the CURRENT
    REQUIREMENT and CURRENT APPLICATION UI.

    ==================================================
    OUTPUT
    ==================================================

    Return valid JSON only.

    {{
        "testcases": [
            {{
                "title": "",
                "preconditions": "",
                "test_steps": "",
                "expected_result": "",
                "priority": ""
            }}
        ]
    }}

    Do not include explanations, comments, or markdown outside the JSON.
    """