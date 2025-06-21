# Entry point to run the bot and dashboard
from flask import Flask, session
from routes.dashboard import dashboard_bp
from routes.callback import callback_bp
from utils.helpers import init_db

app = Flask(__name__)
app.secret_key = "super-secret-key"  # تأكد من جعله سريًا في بيئة الإنتاج

app.register_blueprint(dashboard_bp)
app.register_blueprint(callback_bp)

init_db()



@app.route("/save_welcome", methods=["POST"])
def save_welcome():
    from db.database import SessionLocal
    from db.models import GuildSettings
    db = SessionLocal()

    try:
        guild_id = int(request.form["guild_id"])
        channel_id = request.form["channel_id"]
        welcome_message = request.form["welcome_message"]

        settings = db.query(GuildSettings).filter_by(guild_id=guild_id).first()
        if not settings:
            settings = GuildSettings(guild_id=guild_id)

        settings.welcome_channel_id = channel_id
        settings.welcome_message = welcome_message

        db.add(settings)
        db.commit()

        return "✅ Settings saved."
    except Exception as e:
        print("❌ Error:", e)
        return "❌ Failed", 500
    finally:
        db.close()

