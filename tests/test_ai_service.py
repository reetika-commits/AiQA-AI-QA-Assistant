from unittest.mock import Mock, patch
from app.services.ai_service import generate_testcases

def test_ai_service():
    
    fake_response = {
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

    with patch(
        "app.services.ollama_service.generate_testcases"
    ) as mock_provider,  patch(
        "app.services.ai_service.SQLiteDB"
    ) as mock_db:

        mock_provider.return_value = fake_response

        result = generate_testcases(
            "Generate login test cases",
            "Login requirement",
            "fake_embedding"
        )

    mock_db.return_value.sqlite_procedure.assert_called_once()
    call_args = mock_db.return_value.sqlite_procedure.call_args

    assert call_args.args[0] == "Login requirement"
    assert call_args.args[1] == fake_response["testcases"]
    assert call_args.args[2] == "fake_embedding"

    assert result == fake_response
