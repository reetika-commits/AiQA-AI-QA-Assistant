from ollama import chat
import json


class VisionService():
    def analyze_feature(self,dom,image_path,requirement):
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
            2. A compact representation of the DOM of the same live web application.
            3. The current QA requirement describing what needs to be tested.

            Your task is to identify the UI elements relevant to the CURRENT QA REQUIREMENT,
            using the screenshot and compact DOM as evidence.

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
            3. Use the provided compact DOM to locate the elements corresponding to those UI elements.
            4. Return ONLY the DOM elements that are relevant to the feature shown in the screenshot.
            5. Do not return the complete DOM.
            6. Do not include unrelated elements such as headers, footers, navigation, advertisements, or other page sections unless they are part of the displayed feature.
            7. Prefer elements with useful identifiers such as id, name, class, aria-label, placeholder, onclick, or visible text.
            8. When an element has visible text, preserve that text in the returned element description or DOM representation. Do not replace the visible
            UI label with an event handler or semantic description.
            9. If an element cannot be confidently matched with the DOM, do not invent a selector or DOM element. Mark it as "not_found".
            10. Distinguish between a UI element and its value. For example, "standard_user" is a value entered into a username field; it is not the username field itself.
            11. Return valid JSON only. Do not include explanations outside the JSON.

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

                DOM:{dom},
                images: {image_path},
                CURRENT QA REQUIREMENT:{requirement}
            
            IMPORTANT:
            The CURRENT QA REQUIREMENT determines which functionality is relevant.

            Do not select an element merely because it is visible in the screenshot.
            Select elements that are relevant to fulfilling the CURRENT QA REQUIREMENT.

            The "feature" field should describe the functionality relevant to the requirement.
            Do not treat the feature description as the visible text of a UI element.
            Use the actual DOM information for UI labels, attributes, and selectors.

            The "dom" field should preserve the relevant information from the
            compact DOM, including the element's visible text and useful attributes.
            """
        }],
        format="json"
    )
        print(f"VisionService---->{response}",flush=True)
        return json.loads(response.message.content)

