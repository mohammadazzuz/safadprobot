from flask import Blueprint, render_template, session, request, redirect, url_for
from safadprobot.db.database import SessionLocal
from safadprobot.db.models import GuildSettings

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    if "user_id" not in session:
        print("[DASHBOARD] Session expired. Redirecting to login.")
        return redirect(url_for("callback"))

    db = SessionLocal()

    guilds = session.get("guilds", [])
    selected_guild_id = request.args.get("guild_id")

    if not selected_guild_id and guilds:
        selected_guild_id = guilds[0]["id"]  # أول سيرفر كافتراضي

    if request.method == "POST":
        welcome_channel = request.form.get("channel_id", "")
        welcome_message = request.form.get("welcome_message", "")

        settings = db.query(GuildSettings).filter_by(guild_id=selected_guild_id).first()
        if not settings:
            settings = GuildSettings(guild_id=selected_guild_id)

        settings.welcome_channel_id = welcome_channel
        settings.welcome_message = welcome_message

        db.add(settings)
        db.commit()

        print(f"[DASHBOARD] Updated settings for guild {selected_guild_id}")

    settings = db.query(GuildSettings).filter_by(guild_id=selected_guild_id).first()
    db.close()

    return render_template("dashboard.html",
                            username=session.get("username"),
                            avatar_url=session.get("avatar_url"),
                            guilds=guilds,
                            selected_guild_id=selected_guild_id,
                            settings=settings)
