from unittest.mock import patch, Mock
from app.agents.langgraph_agent import vision_node
from app.agents.langgraph_agent import browser_node
from app.agents.langgraph_agent import route_after_browser
from app.agents.langgraph_agent import qa_graph


def test_browser_node():

    with patch(
        "app.agents.langgraph_agent.BrowserService"
    ) as mock_browser:

        mock_browser.return_value.get_page_text.return_value = "fake page text"
        mock_browser.return_value.get_dom.return_value = "fake full DOM"
        mock_browser.return_value.get_compact_dom.return_value = "fake compact DOM"

        state = {
            "url": "http://test-app.com",
            "image_path": "login.png",
            "requirement": "Verify login",
            "page_text": "",
            "dom": "",
            "compact_dom": "",
            "relevant_dom": "",
            "needs_vision": False
        }

        result = browser_node(state)

        # print("===== BROWSER CALLS =====")
        # print(mock_browser.return_value.mock_calls)

        mock_browser.return_value.open_url.assert_called_once_with(
            "http://test-app.com"
        )
        mock_browser.return_value.get_page_text.assert_called_once()
        mock_browser.return_value.get_dom.assert_called_once()
        mock_browser.return_value.get_compact_dom.assert_called_once()
        mock_browser.return_value.close.assert_called_once()

        assert result == {
            "dom": "fake full DOM",
            "page_text": "fake page text",
            "compact_dom": "fake compact DOM",
            "relevant_dom": "fake compact DOM"
        }

def test_vision_node():

    with patch(
        "app.agents.langgraph_agent.VisionService"
    ) as mock_vision:

        mock_vision.return_value.analyze_feature.return_value = (
            "fake relevant DOM"
        )

        state = {
            "url": "http://test-app.com",
            "image_path": "login.png",
            "requirement": "Verify login",
            "page_text": "fake page text",
            "dom": "fake full DOM",
            "compact_dom": "fake compact DOM",
            "relevant_dom": "",
            "needs_vision": True
        }

        result = vision_node(state)
        # print("===== VISION CALL =====")
        # print(mock_vision.return_value.mock_calls)

        mock_vision.return_value.analyze_feature.assert_called_once_with(
            dom="fake compact DOM",
            image_path="login.png",
            requirement="Verify login"
        )

        assert result == {
            "relevant_dom": "fake relevant DOM"
        }



def test_route_after_browser_needs_vision():

    state = {
        "url": "http://test-app.com",
        "image_path": "login.png",
        "requirement": "Verify login",
        "page_text": "",
        "dom": "",
        "compact_dom": "",
        "relevant_dom": "",
        "needs_vision": True
    }

    result = route_after_browser(state)

    assert result == "vision"

def test_route_after_browser_no_vision():

    state = {
        "url": "http://test-app.com",
        "image_path": "login.png",
        "requirement": "Verify login",
        "page_text": "",
        "dom": "",
        "compact_dom": "",
        "relevant_dom": "",
        "needs_vision": False
    }

    result = route_after_browser(state)

    assert result == "end"



def test_qa_graph_without_vision():

    with patch(
        "app.agents.langgraph_agent.BrowserService"
    ) as mock_browser, patch(
        "app.agents.langgraph_agent.VisionService"
    ) as mock_vision:

        mock_browser.return_value.get_page_text.return_value = "fake page text"
        mock_browser.return_value.get_dom.return_value = "fake full DOM"
        mock_browser.return_value.get_compact_dom.return_value = "fake compact DOM"

        state = {
            "url": "http://test-app.com",
            "image_path": "login.png",
            "requirement": "Verify login",
            "page_text": "",
            "dom": "",
            "compact_dom": "",
            "relevant_dom": "",
            "needs_vision": False
        }

        result = qa_graph.invoke(state)
        mock_vision.return_value.analyze_feature.assert_not_called()


def test_qa_graph_with_vision():

    with patch(
        "app.agents.langgraph_agent.BrowserService"
    ) as mock_browser, patch(
        "app.agents.langgraph_agent.VisionService"
    ) as mock_vision:

        mock_browser.return_value.get_page_text.return_value = "fake page text"
        mock_browser.return_value.get_dom.return_value = "fake full DOM"
        mock_browser.return_value.get_compact_dom.return_value = "fake compact DOM"
        mock_vision.return_value.analyze_feature.return_value = "fake relevant DOM"

        state = {
            "url": "http://test-app.com",
            "image_path": "login.png",
            "requirement": "Verify login",
            "page_text": "",
            "dom": "",
            "compact_dom": "",
            "relevant_dom": "",
            "needs_vision": True
        }

        result = qa_graph.invoke(state)
        mock_vision.return_value.analyze_feature.assert_called_once()
        mock_vision.return_value.analyze_feature.assert_called_once_with(
            dom="fake compact DOM",
            image_path="login.png",
            requirement="Verify login"
        )