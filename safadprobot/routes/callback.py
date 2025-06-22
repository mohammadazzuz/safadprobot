from flask import Blueprint, request, redirect, session, url_for
from sqlalchemy.orm import Session

from safadprobot.db.database import SessionLocal
from safadprobot.db.models import User
from out_oauth.discord_oauth import exchange_code, get_user_data, get_user_guilds

callback = Blueprint("callback", __name__)  # <-- بلوبرنت باسم callback

@callback.route("/callback")
def handle_callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    # Step 1 - Get token
    token_data = exchange_code(code)
    if not token_data:
        return "Failed to get access token", 400

    access_token = token_data["access_token"]
    token_type = token_data["token_type"]

    # Step 2 - Get user info
    user_data = get_user_data(access_token)
    user_id = int(user_data["id"])
    username = f'{user_data["username"]}#{user_data["discriminator"]}'
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{user_data["avatar"]}.png'

    # Step 3 - Get guilds
    guilds = get_user_guilds(access_token)
    manageable_guilds = [g for g in guilds if g.get("permissions", 0) & 0x20]

    # Step 4 - Save session
    session["user_id"] = user_id
    session["username"] = username
    session["avatar_url"] = avatar_url
    session["access_token"] = access_token
    session["token_type"] = token_type

    db = SessionLocal()
    existing_user = db.query(User).filter_by(user_id=user_id).first()
    first_guild_id = manageable_guilds[0]["id"] if manageable_guilds else None

    if not existing_user:
        db.add(User(user_id=user_id, discord_name=username, guild_id=first_guild_id))
    else:
        existing_user.guild_id = first_guild_id
    db.commit()
    db.close()

    if manageable_guilds:
        return redirect(url_for("dashboard.dashboard", guild_id=first_guild_id))
    else:
        return "No manageable guilds found", 400