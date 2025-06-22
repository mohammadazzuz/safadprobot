from flask import Blueprint, render_template, request, session, redirect, url_for
from safadprobot.models import GuildSettings
from safadprobot.database import SessionLocal
from safadprobot.auth.discord_oauth import get_login_url

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(get_login_url())

    db = SessionLocal()
    guilds = session.get("guilds", [])
    if not guilds:
        return redirect(url_for("callback.callback"))  # أو عرض رسالة عدم وجود صلاحية

    selected_guild_id = request.args.get("guild_id") or request.form.get("guild_id")
    settings = None

    if request.method == "POST" and selected_guild_id:
        welcome_channel = request.form.get("channel_id", "")
        welcome_message = request.form.get("welcome_message", "")

        settings = db.query(GuildSettings).filter_by(guild_id=selected_guild_id).first()
        if not settings:
            settings = GuildSettings(guild_id=selected_guild_id)

        settings.welcome_channel_id = welcome_channel
        settings.welcome_message = welcome_message
        db.add(settings)
        db.commit()

    if selected_guild_id:
        settings = db.query(GuildSettings).filter_by(guild_id=selected_guild_id).first()

    db.close()

    return render_template("dashboard.html",
                           username=session.get("username"),
                           avatar_url=session.get("avatar_url"),
                           guilds=guilds,
                           selected_guild_id=selected_guild_id,
                           settings=settings)

