from app.services.browser_service import BrowserService
from app.prompts.agent_prompt import agent_prompt_builder
from app.services.ai_service import generate_testcases
from app.agents.langgraph_agent import qa_graph


#https://www.saucedemo.com/
def agent_generate_testcases(app_url,feature_image,requirements):
    save_url(app_url)
    save_image(feature_image)

    result = qa_graph .invoke({
    "url": app_url,
    "image_path": feature_image,
    "page_text": "",
    "dom": "",
    "relevant_dom": ""
    })

    print(result["relevant_dom"])
    prompt=agent_prompt_builder(result["page_text"],result["relevant_dom"],requirements)
    print(prompt)
    return generate_testcases(prompt,requirements)

def save_url(app_url):
    with open(r"app/sample_data/test_url.txt","w") as fl:
        fl.writelines(app_url)

def save_image(feature_image):

    image_path = "app/sample_data/test_feature_images/" + feature_image.filename

    with open(image_path, "wb") as f:
        f.write(feature_image.file.read())

    print("Image saved:", image_path, flush=True)