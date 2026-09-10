import math
import json
from ollama import embed
from app.database.sqlite_db import SQLiteDB


class RAGService:

    def __init__(self):
        self.db = SQLiteDB()

    def create_embedding(self, story):

        response = embed(
            model="nomic-embed-text",
            input=story
        )

        vector = response["embeddings"][0]

        return vector

    def serialize_embedding(self, vector):
        return json.dumps(vector)

    def deserialize_embedding(self, json_txt):
        return json.loads(json_txt)

    def analyze_requirement(self, requirement):

        needs_vision = True

        print(
            f"---- Inside RAGService: {requirement} ----",
            flush=True
        )

        rows_as_dicts = self.db.get_story_table()

        similar_stories = []

        vector = self.create_embedding(requirement)

        for row in rows_as_dicts:

            similarity = self.cosine_similarity(
                vector,
                self.deserialize_embedding(row["embedding"])
            )

            similar_stories.append({
                "story_id": row["story_id"],
                "title": row["title"],
                "similarity": similarity
            })

        similar_stories.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        print(similar_stories, flush=True)

        top_stories = similar_stories[:2]

        if top_stories and top_stories[0]["similarity"] >= 0.8:
            needs_vision = False

        similar_test_case = self.get_similar_testcases(
            top_stories
        )

        return {
            "rag_result": similar_test_case,
            "embedding": self.serialize_embedding(vector),
            "needs_vision": needs_vision,
            "top_similarity": (
                top_stories[0]["similarity"]
                if top_stories
                else None
            )
        }        


    def get_similar_testcases(self, similar_stories):
        return self.db.get_testcases_table(similar_stories)

    def cosine_similarity(self,a, b):
        dot_product = sum(x * y for x, y in zip(a, b))

        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(y * y for y in b))

        similarity= dot_product / (magnitude_a * magnitude_b)
        
        return similarity

