import chromadb
from app.config import COHERE_API_KEY, metadata_cohere_options
import uuid
import docx2txt

from app.services.embedding_functions.cohere_embedding_function import CohereEmbeddingFunction
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChromaDBService:
    """
    A service class for interacting with ChromaDB.

    Attributes:
        chroma_client (chromadb.PersistentClient): The ChromaDB persistent client.
        collection_name (str): The name of the document collection.
        embedding_function (CohereEmbeddingFunction): The embedding function for document similarity.
        collection (chromadb.Collection): The ChromaDB collection.
    """

    def __init__(self):
        """
        Initializes a new instance of the ChromaDBService class.
        """
        self.chroma_client = chromadb.PersistentClient(path="./chromadb_data")
        self.collection_name = "document_collection" 
        self.embedding_function = CohereEmbeddingFunction(api_key=COHERE_API_KEY)
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata=metadata_cohere_options,
            embedding_function=self.embedding_function
        )

    def get_collection(self):
        """
        Returns the ChromaDB collection.

        Returns:
            chromadb.Collection: The ChromaDB collection.
        """
        return self.collection

    def add_document(self, document):
        """
        Adds a document to the collection.

        Args:
            document: The document to add.

        Returns:
            None
        """
        uuid_name = uuid.uuid1()
        self.collection.add(ids=[uuid_name], documents=[document])

    def add_initial_document(self, docx_path):
        """
        Adds an initial document to the collection.

        Args:
            docx_path (str): The path to the DOCX file.

        Returns:
            None
        """
        content = docx2txt.process(docx_path)

        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=300, chunk_overlap=50
        )

        docs = text_splitter.create_documents([content])

        for doc in docs:
            uuid_name = uuid.uuid1()
            
            self.collection.add(
                ids=[str(uuid_name)], 
                documents=[doc.page_content]
            )

    def query_documents(self, query, n_results=1):
        """
        Queries the collection for documents matching the given query.

        Args:
            query (str): The query string.
            n_results (int): The number of results to return. Defaults to 1.

        Returns:
            list: A list of documents matching the query.
        """
        results = self.collection.query(query_texts=query, n_results=n_results)
        return list(set(results["documents"][0]))

