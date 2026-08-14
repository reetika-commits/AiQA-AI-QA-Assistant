from typing import TypedDict


class QAState(TypedDict):
    url: str
    image_path: str
    page_text: str
    dom: str
    relevant_dom: str

from app.services.browser_service import BrowserService


def browser_node(state: QAState):

    print("===== BROWSER NODE =====", flush=True)

    browser = BrowserService()

    try:
        browser.open_url(state["url"])

        page_text = browser.get_page_text()
        dom = browser.get_dom()
        page_text = browser.get_page_text()

        return {
            "dom": dom,
            "page_text": page_text
        }

    finally:
        browser.close()

from app.services.vision_service import VisionService


def vision_node(state: QAState):

    print("===== VISION NODE =====", flush=True)

    vision_service = VisionService()

    relevant_dom = vision_service.analyze_feature(
        dom=state["dom"]
    )

    return {
        "relevant_dom": relevant_dom
    }

from langgraph.graph import StateGraph, START, END


builder = StateGraph(QAState)

builder.add_node("browser", browser_node)
builder.add_node("vision", vision_node)

builder.add_edge(START, "browser")
builder.add_edge("browser", "vision")
builder.add_edge("vision", END)

qa_graph  = builder.compile()

