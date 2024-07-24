# Home Assignment

## Setup
Create a `.env` file from the `.env.example`

**Note** - you need to provide a valid `OPENAI_API_KEY`

## Run
Use `docker compose` to run the project:
```
docker compose up -d --build
```

## Server API
This server exposes theses endpoints:

- **GET /is_up**: Checks if the Flask server is running.
  - **Response**: Status code 200 if the server is up.

- **POST /ask**: Submits a question to the server.
  - **Request Body**: JSON object containing the question.
  - **Response**: Status code 200 and a JSON object.

**/ask Post Req**
```
{
    curl -X POST http://localhost/ask -H "Content-Type: application/json" -d  '{"question": "Who am I?"}'
}
```

- **GET /qa/{id}**: Retrieves the question and answer for the given `id`.
  - **Response**: Status code 200 and a JSON object.
- 
- **GET /qas/**: Retrieves all questions and answers.
  - **Response**: Status code 200 and a JSON object.

#### A `QuestionAnswer` Object:
```
{
    "id": int
    "question": string
    "answer": string
    "created_at": string
}
```

## Test
### Instal pytest dependencies
Create a venv:
```
 python3 -m venv .venv   
```
Activate venv
```
 source .venv/bin/activate 
```
Install dependencies
```
 pip install -r requirements.txt
```
### Setup
In `conftest.py` make sure `port` and `host` a set to the same ones in the `docker compose`

### Run
```
pytest tests
```

## Development Tools
### Adding migrations
First change a modal in `modals.py`, then run:
```
docker exec -it flask alembic revision --autogenerate -m "<MESSAGE>"
```
### Running migrations
```
docker exec -it flask alembic upgrade head
```