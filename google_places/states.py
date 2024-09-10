from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os
import logging

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base API URL from environment variable (if you plan to externalize)
API_BASE_URL =  "https://countriesnow.space/api/v0.1"

# Define Pydantic models for request body validation
class CountryRequest(BaseModel):
    country: str

class CityRequest(BaseModel):
    country: str
    state: str

@app.post("/fetch-states")
async def fetch_states(request: CountryRequest):
    url = f"{API_BASE_URL}/countries/states"
    payload = json.dumps({
        "country": request.country
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Added timeout for request
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logger.info(f"Successfully fetched states for country: {request.country}")
        return response.json()  # Return the JSON response from the API
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching states for country {request.country}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching states: {str(e)}")
    

@app.post("/fetch-cities")
async def fetch_cities(request: CityRequest):
    url = f"{API_BASE_URL}/countries/state/cities"
    payload = json.dumps({
        "country": request.country,
        "state": request.state
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Added timeout for request
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logger.info(f"Successfully fetched cities for state: {request.state} in country: {request.country}")
        return response.json()  # Return the JSON response from the API
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching cities for state {request.state} in country {request.country}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching cities: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Externalize host/port via environment variables for flexibility
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
