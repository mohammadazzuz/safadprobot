# Flask dashboard routes
from flask import Blueprint, render_template, session, redirect, request
from safadprobot.auth.discord_oauth import exchange_code, get_user_data, get_user_guilds, get_login_url
from safadprobot.db.models import GuildSettings
from safadprobot.db.database import SessionLocal

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    if "user" not in session:
        return redirect(get_login_url())
    return redirect(f"/dashboard?guild_id={guild_id}")



@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    guild_id = request.args.get("guild_id")
    return render_template("dashboard.html", user=session["user"], guild_id=guild_id)


@dashboard_bp.route('/save_welcome', methods=['POST'])
def save_welcome():
    if "user" not in session:
        return redirect("/")

    guild_id = int(request.form.get("guild_id"))
    welcome_channel_id = int(request.form.get("welcome_channel_id"))
    welcome_message = request.form.get("welcome_message")

    print(f"Saved welcome data: {welcome_channel_id}, {welcome_message}")

    # هنا لو عندك قاعدة بيانات، احفظهم فيها.

        # حفظ في قاعدة البيانات
    db = SessionLocal()
    settings = db.query(GuildSettings).filter_by(guild_id=guild_id).first()

    if settings:
        # تحديث إذا موجود
        settings.welcome_channel_id = welcome_channel_id
        settings.welcome_message = welcome_message
    else:
        # إنشاء جديد إذا مش موجود
        settings = GuildSettings(
            guild_id=guild_id,
            welcome_channel_id=welcome_channel_id,
            welcome_message=welcome_message
        )
        db.add(settings)

    db.commit()
    db.close()
    print(f"guild_id = {guild_id} ({type(guild_id)})")


    return redirect(request.referrer or "/dashboard")
