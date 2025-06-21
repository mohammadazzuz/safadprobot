# Flask dashboard routes
from flask import Blueprint, render_template, session, redirect, request
from auth.discord_oauth import generate_login_url

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    if "user" not in session:
        return redirect(generate_login_url())
    return redirect(f"/dashboard?guild_id=YOUR_GUILD_ID")

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    guild_id = request.args.get("guild_id")
    return render_template("dashboard.html", user=session["user"], guild_id=guild_id)
