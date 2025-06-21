# OAuth2 callback logic
from flask import Blueprint, request, redirect, session
from safadprobot.auth.discord_oauth import exchange_code, get_user_data, get_user_guilds, get_login_url

callback_bp = Blueprint("callback", __name__)

@callback_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code from Discord", 400

    token_data = exchange_code(code)
    user_data = get_user_data(token_data["access_token"])

    session["user"] = {
        "id": user_data["id"],
        "username": user_data["username"],
        "discriminator": user_data["discriminator"]
    }

    guilds = get_user_guilds(token_data["access_token"])

    if not guilds:
        return "No guilds found for this user", 400

    # نختار أول سيرفر كافتراضي
    guild_id = guilds[0]["id"]

    print(f"[callback] Selected guild_id: {guild_id}")

    return redirect(f"/dashboard?guild_id={guild_id}")
