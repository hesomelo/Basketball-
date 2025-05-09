from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import cohere
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Basketball Player Comparison API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Pydantic models
class PlayerRequest(BaseModel):
    name: str

class PlayerComparisonRequest(BaseModel):
    player1: str
    player2: str

class PlayerResponse(BaseModel):
    name: str
    summary: str
    stats: Optional[dict] = None

class ComparisonResponse(BaseModel):
    player1: str
    player2: str
    comparison: str

class SimilarPlayersResponse(BaseModel):
    player: str
    similar_players: List[dict]

# Helper functions
async def get_player_stats(name: str) -> dict:
    """Gets player stats from balldontlie API, including season averages"""
    async with httpx.AsyncClient() as client:
        search_url = f"https://www.balldontlie.io/api/v1/players?search={name}"
        response = await client.get(search_url)
        
        if response.status_code != 200 or not response.json()["data"]:
            raise HTTPException(status_code=404, detail="Player not found")
        
        player_id = response.json()["data"][0]["id"]
        stats_url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}"
        stats_response = await client.get(stats_url)
        
        if stats_response.status_code != 200:
            return {}
            
        stats = stats_response.json()["data"]
        return stats[0] if stats else {}

async def generate_player_summary(name: str, stats: dict) -> str:
    """Creates an AI-generated summary of the player's career and style"""
    prompt = f"""Write a concise summary of {name}'s basketball career and playing style. 
    Include their key strengths and notable achievements. Keep it under 200 words."""
    
    response = co.generate(
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    
    return response.generations[0].text.strip()

async def generate_player_comparison(player1: str, player2: str) -> str:
    """Generates an AI comparison between two players"""
    prompt = f"""Compare the playing styles and careers of {player1} and {player2}. 
    Focus on their similarities and differences in terms of:
    1. Playing style
    2. Strengths and weaknesses
    3. Career achievements
    Keep the comparison balanced and objective. Limit to 300 words."""
    
    response = co.generate(
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    
    return response.generations[0].text.strip()

async def find_similar_players(name: str) -> List[dict]:
    """Returns a list of players similar to the given player"""
    # TODO: Implement proper semantic search with player embeddings
    return [
        {"name": "Similar Player 1", "similarity_score": 0.85},
        {"name": "Similar Player 2", "similarity_score": 0.82},
        {"name": "Similar Player 3", "similarity_score": 0.78}
    ]

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Basketball Player Comparison API"}

@app.post("/player/summary", response_model=PlayerResponse)
async def get_player_summary(request: PlayerRequest):
    try:
        stats = await get_player_stats(request.name)
        summary = await generate_player_summary(request.name, stats)
        return PlayerResponse(
            name=request.name,
            summary=summary,
            stats=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/player/compare", response_model=ComparisonResponse)
async def compare_players(request: PlayerComparisonRequest):
    try:
        comparison = await generate_player_comparison(request.player1, request.player2)
        return ComparisonResponse(
            player1=request.player1,
            player2=request.player2,
            comparison=comparison
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/player/similar", response_model=SimilarPlayersResponse)
async def get_similar_players(request: PlayerRequest):
    try:
        similar_players = await find_similar_players(request.name)
        return SimilarPlayersResponse(
            player=request.name,
            similar_players=similar_players
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 