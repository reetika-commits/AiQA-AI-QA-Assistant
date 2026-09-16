from app.services.rag_service import RAGService
from unittest.mock import Mock, patch
import json

def test_cosine_similarity():

    rag = RAGService()

#"How semantically similar is this new requirement to an old requirement?"
    result = rag.cosine_similarity(
        [1, 0],
        [1, 0]
    )
    
    assert result == 1

    result = rag.cosine_similarity(
        [1, 0],
        [-1, 0]
    )

    assert result == -1

    result = rag.cosine_similarity(
    [1, 0],
    [0, 1]
    )

    assert result == 0

# flow:
#              TEST
#                │
#        "Verify login"
#                ↓
#        analyze_requirement()
#           ↙           ↘
#    fake Ollama       fake DB
#        ↓                ↓
#  [1, 0]          fake story rows
#           \          /
#            cosine_similarity
#                 ↓
#              real logic

def test_analyze_requirement_embedding_and_story():

    fake_story = {
        "story_id": 1,
        "title": "Verify login",
        "embedding": "[1, 0]"
    }

    fake_testcases = [ 
    {
        "title": "Verify login",
        "test_steps": "Enter username and password",
        "expected_result": "User should login successfully",
        "priority": "High"
    }
    ] #list of dictionary

    with patch(
        "app.services.rag_service.embed"
    ) as mock_embed, patch(
        "app.services.rag_service.SQLiteDB"
    ) as mock_db:

        mock_embed.return_value = {
            "embeddings": [[-1, 0]]   ###for similarity to be -1, i.e <80 and needs_vision True
            #"embeddings": [[1, 0]]   ###for similarity to be 1, i.e >=80 and needs_vision false
            
        }

        mock_db.return_value.get_story_table.return_value = [
            fake_story
        ]

        mock_db.return_value.get_testcases_table.return_value = [
                    fake_testcases
                ]
        

        rag = RAGService()

        result = rag.analyze_requirement("Verify login")
        mock_db.return_value.get_testcases_table.assert_called_once()
        call_args=mock_db.return_value.get_testcases_table.call_args
        assert call_args.args[0] == [
        {
            "story_id": 1,
            "title": "Verify login",
            "similarity": -1.0
        }
        ]
        assert result["rag_result"] == [fake_testcases]
        assert result["top_similarity"] == -1.0
        assert result["needs_vision"] is True
        assert json.loads(result["embedding"]) == [-1, 0]
        

def test_analyze_requirement_selects_top_two_stories():
    fake_stories = [
    {
        "story_id": 1,
        "title": "Story A",
        "embedding": "[1, 0]"
    },
    {
        "story_id": 2,
        "title": "Story B",
        "embedding": "[0, 1]"
    },
    {
        "story_id": 3,
        "title": "Story C",
        "embedding": "[-1, 0]"
    }
    ]

    with patch(
            "app.services.rag_service.embed"
        ) as mock_embed, patch(
            "app.services.rag_service.SQLiteDB"
        ) as mock_db:
    
            mock_embed.return_value = {
                "embeddings": [[1, 0]]
            }

            mock_db.return_value.get_story_table.return_value=fake_stories
            mock_db.return_value.get_testcases_table.return_value=[]

            rag = RAGService()

            result = rag.analyze_requirement("Verify login")
            # print(result["top_similarity"])

            call_args = mock_db.return_value.get_testcases_table.call_args

            # print(call_args.args[0])

            assert call_args.args[0] == [
            {
                "story_id": 1,
                "title": "Story A",
                "similarity": 1.0
            },
            {
                "story_id": 2,
                "title": "Story B",
                "similarity": 0.0
            }
            ]
            assert len(call_args.args[0])==2

def test_analyze_requirement_vision_threshold():
    fake_story = {
        "story_id": 1,
        "title": "Verify login",
        "embedding": "[1, 0]"
    }

    
    with patch( #"Find this thing- embed at this MODULE PATH and replace with mock"
        "app.services.rag_service.embed"
    ) as mock_embed, patch( ##"Find this thing- SQLiteDB at this MODULE PATH and replace with mock"
        "app.services.rag_service.SQLiteDB"
    ) as mock_db, patch.object( #"Take THIS OBJECT-RAGService and replace THIS ATTRIBUTE-cosine_similarity, set return value =0.79"
        RAGService,
        "cosine_similarity",
        return_value=0.8 # 0.79
    ) as mock_similarity:

        mock_embed.return_value = {
            "embeddings": [[1, 0]]
        }

        mock_db.return_value.get_story_table.return_value = [
            fake_story
        ]

        mock_db.return_value.get_testcases_table.return_value = []
        rag = RAGService()

        result = rag.analyze_requirement("Verify login")

        #boundry value test for if (top_similarity >=80)
        assert result["top_similarity"] == 0.8
        assert result["needs_vision"] is False
        # assert result["top_similarity"] == 0.79
        # assert result["needs_vision"] is True
