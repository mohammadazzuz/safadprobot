# OAuth2 callback logic
from flask import Blueprint, request, redirect, session
from safadprobot.auth.discord_oauth import get_access_token, get_user_info

callback_bp = Blueprint("callback", __name__)

@callback_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code from Discord", 400

    token_data = get_access_token(code)
    user_data = get_user_info(token_data["token_type"], token_data["access_token"])

    session["user"] = {
        "id": user_data["id"],
        "username": user_data["username"],
        "discriminator": user_data["discriminator"]
    }

    return redirect(f"/dashboard?guild_id=YOUR_GUILD_ID")
