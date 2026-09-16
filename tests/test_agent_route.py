from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_call_agent_success():

    # step 1: create fake response
    fake_response = {
        "LLM_response": {
            "testcases": [
                {
                    "title": "Verify login",
                    "priority": "High"
                }
            ]
        },
        "needs_vision": False,
        "top_similarity": 1.0,
        "relevant_dom": "fake DOM"
    }

    # step 2: patch
    with patch(
        "app.routes.agent_route.agent_generate_testcases"
    ) as mock_agent:

        # step 3: set return value to fake response
        mock_agent.return_value = fake_response

        # step 4: get data from API, URL, Screenshot and requirement
        response = client.post(
            "/agent/test-features",
            data={
                "web_app_url": "http://test-app.com",
                "requirements": "Verify login"
            },
            files={
                "feature_image": (
                    "login.png",
                    b"fake image data",
                    "image/png"
                )
            }
        )

        # step 5: assert status code
        assert response.status_code == 200

        # step 5: call agent and print arguments
        mock_agent.assert_called_once()
        # print("===== AGENT CALL =====")
        # print(mock_agent.call_args)

        # step 6: collect arguments to assert
        agent_call = mock_agent.call_args

        # step 7: assert arguments
        assert agent_call.args[0] == "http://test-app.com"
        assert agent_call.args[1].filename == "login.png"
        assert agent_call.args[2] == "Verify login"

        # step 8: assert response from agent
        assert response.json() == {
            "checkpoint": "QA AGENT COMPLETED",
            "response": fake_response
        }

def test_call_agent_missing_requirements():

    with patch(
        "app.routes.agent_route.agent_generate_testcases"
    ) as mock_agent:

        response = client.post(
            "/agent/test-features",
            data={
                "web_app_url": "http://test-app.com"
                # requirements intentionally missing
            },
            files={
                "feature_image": (
                    "login.png",
                    b"fake image data",
                    "image/png"
                )
            }
        )

        # print("===== VALIDATION RESPONSE =====")
        # print(response.status_code)
        # print(response.json())

        assert response.status_code == 422
        mock_agent.assert_not_called()
        mock_agent.side_effect = Exception("Agent failed")
        

def test_call_agent_agent_failure():

    with patch(
        "app.routes.agent_route.agent_generate_testcases"
    ) as mock_agent:

        mock_agent.side_effect = Exception("Agent failed")

        response = client.post(
            "/agent/test-features",
            data={
                "web_app_url": "http://test-app.com",
                "requirements": "Verify login"
            },
            files={
                "feature_image": (
                    "login.png",
                    b"fake image data",
                    "image/png"
                )
            }
        )
        # print("===== FAILURE RESPONSE =====")
        # print(response.status_code)
        # print(response.json())
        assert response.status_code == 500

        assert response.status_code == 500

        body = response.json()

        assert body["detail"] == "QA Agent failed"

        mock_agent.assert_called_once()