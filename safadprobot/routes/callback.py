import os
import requests
from flask import request, redirect, session, url_for
from safadprobot.db.database import SessionLocal
from safadprobot.db.models import User
from safadprobot.auth.discord_oauth import exchange_code, get_user_data, get_user_guilds



DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

def handle_callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    # Step 1: Exchange code for token
    token_data = exchange_code(code)
    access_token = token_data.get("access_token")
    token_type = token_data.get("token_type")

    if not access_token:
        return "Failed to get access token", 400

    # Step 2: Get user info
    user_data = get_user_data(token_type, access_token)
    user_id = int(user_data.get("id"))
    username = f"{user_data.get('username')}#{user_data.get('discriminator')}"
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data.get('avatar')}.png"

    # Step 3: Get user guilds
    guilds = get_user_guilds(token_type, access_token)
    manageable_guilds = [g for g in guilds if g.get("permissions", 0) & 0x20]

    # Step 4: Save to session
    session["user_id"] = user_id
    session["username"] = username
    session["avatar_url"] = avatar_url
    session["guilds"] = manageable_guilds
    session["access_token"] = access_token
    session["token_type"] = token_type

    print(f"[AUTH] Logged in as: {username} ({user_id})")
    print(f"[AUTH] Guilds with manage perms: {len(manageable_guilds)}")

    # Step 5: Add user to DB if not exists
    db = SessionLocal()
    existing_user = db.query(User).filter_by(user_id=user_id).first()
    if not existing_user:
        print(f"[DB] New user. Adding {username}")
        new_user = User(user_id=user_id, discord_name=username, guild_id=None)
        db.add(new_user)
        db.commit()
    else:
        print(f"[DB] Existing user: {username}")

    db.close()

    return redirect(url_for("dashboard"))
