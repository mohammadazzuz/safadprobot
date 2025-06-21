import os
import requests
from urllib.parse import urlencode

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

BASE_URL = "https://discord.com/api"

SCOPES = ["identify", "guilds", "bot"]

def get_login_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "permissions": 8,
        "prompt": "consent"  # بيخليه يعرض صفحة الإضافة كل مرة
    }
    return f"{BASE_URL}/oauth2/authorize?{urlencode(params)}"

def exchange_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(f"{BASE_URL}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    return r.json()

def get_user_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"{BASE_URL}/users/@me", headers=headers)
    r.raise_for_status()
    return r.json()

def get_user_guilds(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"{BASE_URL}/users/@me/guilds", headers=headers)
    r.raise_for_status()
    return r.json()
