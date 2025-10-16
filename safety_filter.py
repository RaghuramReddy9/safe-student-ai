import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PERSPECTIVE_API_KEY")

ATTRIBUTES = {
    "TOXICITY": {},
    "INSULT": {},
    "THREAT": {},
    "SEXUALLY_EXPLICIT": {},
}

def analyze_text(text: str) -> dict:
    """Send text to Perspective API and return all scores."""
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": ATTRIBUTES
    }

    response = requests.post(url, json=data)
    result = response.json()

    scores = {}
    for attr in ATTRIBUTES:
        scores[attr] = result["attributeScores"][attr]["summaryScore"]["value"]

    return scores
