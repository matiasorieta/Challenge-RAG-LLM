# README

This is an app that responds to a question about a document using the RAG architecture.

## Getting Started Locally

To get started with this Flask app locally, follow the instructions below:

1. Clone the repository to your local machine.
2. Navigate to the source directory of the app.
3. Create a virtual environment by running the following command:
    ```
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows, run:
        ```
        venv\Scripts\activate
        ```
    - On macOS and Linux, run:
        ```
        source venv/bin/activate
        ```
5. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```
6. Run the Flask app by executing the following command:
    ```
    python run.py
    ```
7. Open your web browser and navigate to `http://localhost:5000` to access the app.

## Getting Started with Docker

To get started with this Flask app using Docker, follow the instructions below:

1. Clone the repository to your local machine.
2. Navigate to the source directory of the app.
3. Build the Docker image by running the following command:
    ```
    docker build -t flask-app .
    ```
4. Run the Docker container by executing the following command:
    ```
    docker run -p 5000:5000 flask-app
    ```
5. Open your web browser and navigate to `http://localhost:5000` to access the app.

## Routes

The Flask app has the following routes:

- `/` (GET): This is the index route of the Flask app. It returns a simple 'Question Answering API - Cohere' message.
- `/ask` (POST): This route allows users to ask a new question and submit it for answering. It expects a JSON payload with the following structure:

```json
{
    "user_name": "John Doe",
    "question": "How are you today?"
}
```

The route will return a JSON response with the answer to the submitted question:

```json
{
    "answer": "answer"
}
```
```
