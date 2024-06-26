import cohere
from typing import List

class CohereEmbeddingFunction:
    """
    A class that represents a Cohere embedding function.

    Attributes:
        api_key (str): The API key for accessing the Cohere API.
        model (str): The name of the model to use for embedding. Default is "multilingual-22-12".
    """

    def __init__(self, api_key: str, model: str = "multilingual-22-12"):
        """
        Initializes a CohereEmbeddingFunction object.

        Args:
            api_key (str): The API key for accessing the Cohere API.
            model (str, optional): The name of the model to use for embedding. Default is "multilingual-22-12".
        """
        self.client = cohere.Client(api_key=api_key)
        self.model = model

    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Embeds a list of input texts using the Cohere API.

        Args:
            input (List[str]): The list of input texts to embed.

        Returns:
            List[List[float]]: The embedded representations of the input texts.
        """
        res = self.client.embed(
            texts=input,
            model=self.model,
            input_type="search_query",
            embedding_types=['float']
        )
        return res.embeddings.float_