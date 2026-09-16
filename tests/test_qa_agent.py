from unittest.mock import patch, Mock
from app.agents.qa_agent import agent_generate_testcases

def test_agent_generate_testcases():

    fake_image = Mock()
    fake_image.filename = "login.png"
    fake_image.file.read.return_value = b"fake image data"

    #### Patch -> create MagicMock
    with patch("app.agents.qa_agent.RAGService"
        ) as mock_rag, patch("app.agents.qa_agent.generate_testcases"
        ) as mock_llm, patch("app.agents.qa_agent.qa_graph.invoke"
        ) as mock_graph, patch("app.agents.qa_agent.vision_prompt_builder"
        ) as mock_vision_prompt, patch("app.agents.qa_agent.rag_prompt_builder"
        ) as mock_rag_prompt:

    ### Set return values
        mock_vision_prompt.return_value = "fake vision prompt"

        mock_rag.return_value.analyze_requirement.return_value = {
            "rag_result": [],
            "embedding": "[1, 0]",
            "needs_vision": True,
            "top_similarity": 0.5
            }

        mock_llm.return_value = {
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

        mock_graph.return_value = {
            "relevant_dom": "fake relevant DOM",
            "compact_dom": "fake compact DOM"
            }

        
        ### CAlls with argumrnts, were needed
        # main funtion
        result = agent_generate_testcases(
                "http://test-app.com",
                fake_image,
                "Verify login"
                )

        # RAG_service
        mock_rag.return_value.analyze_requirement.assert_called_once_with("Verify login")

        #graph
        graph_call = mock_graph.call_args_list[0]

        #Vision Prompt
        mock_vision_prompt.assert_called_once_with(
                    "Verify login",
                    "fake relevant DOM",
                    []
                )

        #RAg prompt
        mock_rag_prompt.assert_not_called()      

        #LLM
        mock_llm.assert_called_once()
        llm_call=mock_llm.call_args_list[0]

        # print("===== GRAPH CALL =====")
        # print("MAgicMock: mock_graph:", mock_graph)
        # print("Mock: fake_image",fake_image)
        # print("mock_graph.call_count:", mock_graph.call_count)
        # print("mock_graph.mock_calls:", mock_graph.mock_calls)
        # print("fake_image.mock_calls:", fake_image.mock_calls)
        # print(graph_call)
        # print("ARGS:", graph_call.args)
        # print("KWARGS:", graph_call.kwargs)

        ### asserts
        assert graph_call.args[0]["requirement"] == "Verify login"
        assert graph_call.args[0]["needs_vision"] is True
        assert graph_call.args[0]["url"] =="http://test-app.com"
        assert graph_call.args[0]["image_path"].endswith("login.png")

        assert llm_call.args[1]=="Verify login"
        assert llm_call.args[2]=="[1, 0]"

        assert llm_call.args[0] == "fake vision prompt"

        assert result == {
        "LLM_response": mock_llm.return_value,
        "needs_vision": True,
        "top_similarity": 0.5,
        "relevant_dom": "fake relevant DOM"
        }
