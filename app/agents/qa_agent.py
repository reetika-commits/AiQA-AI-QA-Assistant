from app.prompts.rag_promt import rag_prompt_builder
from app.prompts.rag_promt import vision_prompt_builder
from app.services.ai_service import generate_testcases
from app.agents.langgraph_agent import qa_graph
from app.services.rag_service import RAGService


def agent_generate_testcases(app_url, feature_image, requirements):

    try:
        # print("---- Inside qa_agent -> saving URL and Image ----")

        save_url(app_url)
        image_path = save_image(feature_image)

        # print(
        #     "---- Inside qa_agent -> creating RAGService "
        #     "and calling new_story ----"
        # )

        rag = RAGService()
        rag_dict = rag.analyze_requirement(requirements)

        # print("---- Inside qa_agent -> Invoking LangGraph ----")

        result = qa_graph.invoke({
            "url": app_url,
            "image_path": image_path,
            "requirement": requirements,
            "page_text": "",
            "dom": "",
            "compact_dom":"",
            "relevant_dom": "",
            "needs_vision": rag_dict["needs_vision"]
        })

        # print(
        #     f"--- Inside qa_agent -> DOM: "
        #     f"{result['relevant_dom']}" 
        # )

        # print(
        #     f"--- Inside qa_agent -> RAG Result: "
        #     f"{len(rag_dict['rag_result'])}"
        # )

        if rag_dict["needs_vision"]:

            prompt = vision_prompt_builder(
                requirements,
                result["relevant_dom"],
                rag_dict["rag_result"]
            )

        else:

            prompt = rag_prompt_builder(
                requirements,
                result["relevant_dom"],
                rag_dict["rag_result"]
            )

        # print(
        #     f"---- Inside qa_agent -> relevant_dom -> {result["relevant_dom"]}"
        )

        llm_response = generate_testcases(
            prompt,
            requirements,
            rag_dict["embedding"]
        )

        return {
            "LLM_response": llm_response,
            "needs_vision": rag_dict["needs_vision"],
            "top_similarity": rag_dict["top_similarity"],
            "relevant_dom": result["relevant_dom"]
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise

def save_url(app_url):
    with open(r"app/sample_data/test_url.txt","w") as fl:
        fl.writelines(app_url)

def save_image(feature_image):
    image_path = (
        "app/sample_data/test_feature_images/"
        + feature_image.filename
    )

    with open(image_path, "wb") as f:
        f.write(feature_image.file.read())

    # print("Image saved:", image_path, flush=True)

    return image_path