from unittest.mock import patch, Mock
from app.services.ollama_service import generate_testcases
from app.config.settings import OLLAMA_MODEL

def test_generate_testcases():
    prompt = "Generate login test cases"

    fake_response = Mock()
    fake_response.message.content = """
    {
        "testcases": [
            {
                "title": "Verify login",
                "preconditions": "User is on login page",
                "test_steps": "Enter username and password",
                "expected_result": "User should login successfully",
                "priority": "High"
            }
        ]
    }
    """
    with patch("app.services.ollama_service.chat") as mock_chat:
        mock_chat.return_value = fake_response

        result = generate_testcases(prompt)

        mock_chat.assert_called_once()
        call_args = mock_chat.call_args

        assert call_args.kwargs["model"] == OLLAMA_MODEL
        assert call_args.kwargs["format"] == "json"
        assert call_args.kwargs["messages"][0]["content"] == "Generate login test cases"

    assert result["testcases"][0]["title"] == "Verify login"

