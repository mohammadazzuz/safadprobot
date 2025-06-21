# Flask dashboard routes
from flask import Blueprint, render_template, session, redirect, request
from safadprobot.auth.discord_oauth import get_login_url

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    if "user" not in session:
        return redirect(get_login_url())
    return redirect(f"/dashboard?guild_id=YOUR_GUILD_ID")



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

    welcome_channel_id = request.form.get("welcome_channel_id")
    welcome_message = request.form.get("welcome_message")

    print(f"Saved welcome data: {welcome_channel_id}, {welcome_message}")
    # هنا لو عندك قاعدة بيانات، احفظهم فيها.

    return redirect(request.referrer or "/dashboard")
