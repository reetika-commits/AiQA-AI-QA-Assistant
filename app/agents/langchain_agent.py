# from langchain.agents import create_agent
# from langchain.tools import tool
# from langchain_ollama import ChatOllama
# from app.services.browser_service import BrowserService
# from app.services.vision_service import VisionService

# url="https://www.saucedemo.com/"
# image_path="app/sample_data/test_feature_images/saucedemo log in.png"

# @tool
# def get_application_info(url: str) -> str:
#     """Open the application URL and return the page text and DOM."""

#     print("===== GET APPLICATION INFO TOOL CALLED =====", flush=True)

#     driver = BrowserService()
#     driver.open_url(url)

#     page_text = driver.get_page_text()
#     dom = driver.get_dom()
#     driver.close()

#     return f"""
#         PAGE TEXT:
#         {page_text}

#         DOM:
#         {dom}
#         """


# llm = ChatOllama(
#     model="qwen3:8b"
# )

# @tool
# def analyze_feature(dom: str) -> str:
#     """Analyze the feature screenshot against the application DOM and return the relevant DOM elements."""
#     print("===== ANALYZE FEATURE TOOL CALLED =====", flush=True)
#     vision_service = VisionService()

#     return vision_service.analyze_feature(
#             dom=dom
#     )

# agent = create_agent(
#     model=llm,
#     tools=[
#         get_application_info,
#         analyze_feature
#         ],
#     system_prompt = """
#             You are a QA automation agent.

#             Your task is to inspect a web application's feature and identify
#             the relevant DOM elements for that feature.

#             When given a URL and feature screenshot, follow this sequence strictly:

#             1. First call get_application_info with the application URL.
#             2. Wait for the result from get_application_info.
#             3. The result will contain the page text and DOM.
#             4. Then call analyze_feature and pass the DOM returned by
#             get_application_info as the `dom` argument.
#             5. Do not call analyze_feature before receiving the result
#             from get_application_info.
#             6. Do not pass the image path as the `dom` argument.
#             7. After analyze_feature returns the relevant DOM elements,
#             return that result to the caller.
#             8. Do not generate test cases.

#             The feature screenshot is already available to the vision analysis
#             tool. You do not need to pass the image path to analyze_feature.
#             """
# )

# result = agent.invoke({
#     "messages": [
#         {
#             "role": "user",
#             "content": f"""
#             Inspect the specified feature of this web application.

#             URL: {url}

#             Feature screenshot: {image_path}

#             Return only the relevant DOM elements for this feature.
#             """
#         }
#     ]
# })

# print("\n===== MESSAGE FLOW =====")

# for i, message in enumerate(result["messages"]):
#     print(f"\n--- Message {i} ---")
#     print("TYPE:", type(message).__name__)
#     print("CONTENT:", message.content)

#     if hasattr(message, "tool_calls"):
#         print("TOOL CALLS:", message.tool_calls)