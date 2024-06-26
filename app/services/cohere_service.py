import cohere
import json
import re
from app.config import COHERE_API_KEY
from app.services.chromadb_service import ChromaDBService

class CohereService:
    """
    A class that provides methods to interact with the Cohere API for generating answers to questions.

    Attributes:
        cohere_client (cohere.Client): The Cohere client for making API requests.
        chromadb_service (ChromaDBService): The ChromaDB service for querying documents.
        model (str): The model to be used for generating answers.

    """

    def __init__(self, model="command-r"):
        """
        Initializes a new instance of the CohereService class.

        Args:
            model (str, optional): The model to be used for generating answers. Defaults to "command-r".

        """
        self.cohere_client = cohere.Client(api_key=COHERE_API_KEY)
        self.chromadb_service = ChromaDBService()
        self.model = model

    def generate_prompt(self, question):
        """
        Generates a prompt for the Cohere service based on the provided question.

        Args:
            question (str): The input question.

        Returns:
            str: The generated prompt.

        """
        prompt = f"""
        ## Instructions
        Based on the provided documents perform the following steps:
        1. Read the documents provided. Ignore the language of the documents.
        2. Read the input question provided.
        3. Detect the language of the question. 
        4. Provide an answer to the question. The answer should be in the same language that the question, one sentence long, and always in third person.
        5. Append to the answer emojis that best summarizes the answer.

        ## Output
        Output the answer in the following JSON format: 
        \\{{"question": "<question>", "language_question": "<language of the question>", "answer": "<your answer in the language of the question>", "emojis": "<utf-8 emojis>"\\}}

        ## Example
        Input question: "who is Emma?"
        Answer: \\{{"question": "who is Emma?", "language_question": "english", "answer": "Emma is a software engineer.", "emojis": "👩‍💻"\\}}

        ## Input question:
        {question}        
        """
        return prompt.strip()

    
    def generate_documents(self, documents):
        """
        Generate a list of documents from the given input.

        Args:
            documents (list): A list of strings representing documents in the format "title: content".

        Returns:
            list: A list of dictionaries, where each dictionary represents a document with keys "title" and "snippet".
        """
        document_list = []
        for document in documents:
            title, content = document.split(":")
            document_list.append({
                "title": title.strip(),
                "snippet": content.strip()
            })

        return document_list
    
    def get_json(self, answer):
        """
        Parses the given answer string and returns the corresponding JSON object.

        Args:
            answer (str): The answer string to be parsed.

        Returns:
            dict: The parsed JSON object.

        Raises:
            KeyError: If the answer string does not contain a valid JSON object.
            json.JSONDecodeError: If the answer string cannot be decoded as JSON.

        """
        answer_cleaned = answer.strip("```json\n").strip("\n```").replace('\n', '').replace('\xa0', '')
        try:
            answer_json = json.loads(answer_cleaned)
        except (KeyError, json.JSONDecodeError):
            match = re.search(r'{.*}', answer_cleaned, re.DOTALL)
            if match:
                json_content = match.group(0)
                try:
                    answer_json = json.loads(json_content)
                except json.JSONDecodeError:
                    return {"error": "Failed to parse service response."}, 500
            else:
                return {"error": "Failed to parse service response."}, 500
        return answer_json

    def get_answer(self, question):
        """
        Retrieves an answer to the given question using the Cohere API.

        Args:
            question (str): The question to be answered.

        Returns:
            str: The answer to the question along with associated emojis.
        """

        results = self.chromadb_service.query_documents(question, 3)

        documents = self.generate_documents(results)
        prompt = self.generate_prompt(question)

        final_answer = self.cohere_client.chat(
            message=prompt,
            documents=documents,
            model=self.model,
            temperature=0,
            seed=40
        )

        result_json = self.get_json(final_answer.text)
        
        return result_json["answer"] + " " + result_json["emojis"]
