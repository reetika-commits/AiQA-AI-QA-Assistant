from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from app.services.browser_service import BrowserService
from app.services.vision_service import VisionService


class QAState(TypedDict):
    url: str
    image_path: str
    requirement: str
    page_text: str
    dom: str
    compact_dom:str
    relevant_dom: str
    needs_vision: bool


def browser_node(state: QAState):
    # print("===== BROWSER NODE =====", flush=True)

    browser = BrowserService()

    try:
        browser.open_url(state["url"])

        page_text = browser.get_page_text()
        dom = browser.get_dom()
        compact_dom=browser.get_compact_dom()

        return {
            "dom": dom,
            "page_text": page_text,
            "compact_dom":compact_dom,
            "relevant_dom": compact_dom
        }

    finally:
        browser.close()


def route_after_browser(state: QAState):

    if state["needs_vision"]:
        return "vision"

    return "end"


def vision_node(state: QAState):
    # print("===== VISION NODE =====", flush=True)

    dom = state["compact_dom"]
    image_path = state["image_path"]
    requirement = state["requirement"]

    # print("===== VISION DOM SIZE =====", flush=True)
    # print(f"Compact DOM :{dom}", flush=True)
    # print(f"Compact DOM characters: {len(dom)}", flush=True)
    # print(f"Image path: {image_path}", flush=True)
    # print("===========================", flush=True)

    vision_service = VisionService()

    relevant_dom = vision_service.analyze_feature(
        dom=dom,
        image_path=image_path,
        requirement=requirement
    )

    # print(
    #     f"Relevant DOM characters: {len(str(relevant_dom))}",
    #     flush=True
    # )

    return {
        "relevant_dom": relevant_dom
    }

builder = StateGraph(QAState)

builder.add_node("browser", browser_node)
builder.add_node("vision", vision_node)

builder.add_edge(START, "browser")

builder.add_conditional_edges(
    "browser",
    route_after_browser,
    {
        "vision": "vision",
        "end": END
    }
)

builder.add_edge("vision", END)

qa_graph = builder.compile()