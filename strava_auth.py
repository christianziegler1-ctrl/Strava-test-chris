"""
Strava OAuth2 Authentifizierung
Führe dieses Script einmalig aus, um deinen Refresh Token zu erhalten.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"


def get_authorization_url():
    """Gibt die URL zurück, die der User besuchen muss."""
    scope = "read,activity:read_all"
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={scope}"
    )
    return url


def exchange_code_for_token(code: str) -> dict:
    """Tauscht den Auth-Code gegen Access + Refresh Token."""
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    response.raise_for_status()
    return response.json()


def refresh_access_token(refresh_token: str) -> dict:
    """Erneuert den Access Token mit dem Refresh Token."""
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    response.raise_for_status()
    return response.json()


def get_valid_access_token() -> str:
    """Gibt einen gültigen Access Token zurück (erneuert bei Bedarf)."""
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
    if not refresh_token:
        raise ValueError("STRAVA_REFRESH_TOKEN nicht in .env gesetzt!")

    token_data = refresh_access_token(refresh_token)
    return token_data["access_token"]


if __name__ == "__main__":
    print("=== Strava Erstmalige Authentifizierung ===")
    print()
    print("Schritt 1: Besuche diese URL in deinem Browser:")
    print()
    print(get_authorization_url())
    print()
    print("Schritt 2: Nach der Genehmigung wirst du weitergeleitet.")
    print("Kopiere den 'code' Parameter aus der URL (z.B. ?code=XXXXX)")
    print()
    code = input("Füge den Code hier ein: ").strip()

    token_data = exchange_code_for_token(code)
    print()
    print("Erfolg! Deine Token-Daten:")
    print(f"  Access Token:  {token_data['access_token'][:20]}...")
    print(f"  Refresh Token: {token_data['refresh_token']}")
    print()
    print("Füge folgende Zeilen in deine .env Datei ein:")
    print(f"STRAVA_REFRESH_TOKEN={token_data['refresh_token']}")
    print(f"STRAVA_ACCESS_TOKEN={token_data['access_token']}")
