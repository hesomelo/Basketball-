# Basketball Player Comparison API

A FastAPI-based backend service that provides AI-powered basketball player comparisons, summaries, and similar player recommendations using the Cohere API.

## Features

- Get AI-generated summaries of basketball players
- Compare two players with AI-generated insights
- Find similar players based on playing style and characteristics
- Integration with balldontlie API for player statistics

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your API keys:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   BALLDONTLIE_API_KEY=your_balldontlie_api_key_here
   ```

## Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Get Player Summary
- **POST** `/player/summary`
- **Body**: `{"name": "player name"}`

### Compare Players
- **POST** `/player/compare`
- **Body**: `{"player1": "name1", "player2": "name2"}`

### Find Similar Players
- **POST** `/player/similar`
- **Body**: `{"name": "player name"}`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Technologies Used

- FastAPI
- Cohere API
- balldontlie API
- Python 3.8+
- Pydantic
- httpx 