from ollama import chat
import json

feature_image_path="app/sample_data/test_feature_images/saucedemo log in.png"

class VisionService():
    def analyze_feature(self,dom):
        print("inside vision Service")
        response = chat(
        model="qwen2.5vl:3b",
        messages=[
            {
                "role": "user",
            "content": f"""
            You are a UI analysis assistant for an AI-powered QA automation system.

            You will receive:
            1. A screenshot of a web application's feature.
            2. The DOM/page source of the same live web application.

            Your task is to identify the feature shown in the screenshot and find the corresponding UI elements in the provided DOM.

            Instructions:

            1. Analyze the screenshot and identify the main feature/functionality being shown.
            2. Identify the important interactive UI elements visible in the screenshot, such as:
            - text fields
            - password fields
            - buttons
            - links
            - checkboxes
            - radio buttons
            - dropdowns
            - other controls
            3. Use the DOM to locate the elements corresponding to those UI elements.
            4. Return ONLY the DOM elements that are relevant to the feature shown in the screenshot.
            5. Do not return the complete DOM.
            6. Do not include unrelated elements such as headers, footers, navigation, advertisements, or other page sections unless they are part of the displayed feature.
            7. Prefer elements with useful identifiers such as id, name, class, aria-label, placeholder, or visible text.
            8. If an element cannot be confidently matched with the DOM, do not invent a selector or DOM element. Mark it as "not_found".
            9. Distinguish between a UI element and its value. For example, "standard_user" is a value entered into a username field; it is not the username field itself.
            10. Return valid JSON only. Do not include explanations outside the JSON.

            Return the result in exactly this structure:

            {{
                "feature": "",
                "elements": [
                    {{
                        "type": "",
                        "description": "",
                        "selector": "",
                        "dom": "",
                        "status": "found"
                    }}
                ]
            }}

            For elements that cannot be matched:

            {{
                "type": "",
                "description": "",
                "selector": "",
                "dom": "",
                "status": "not_found"
            }}

            DOM:{dom}
            """,
                "images": [feature_image_path]
            }
        ],
        format="json"
    )
        print(f"VisionService---->{response}",flush=True)
        return json.loads(response.message.content)

