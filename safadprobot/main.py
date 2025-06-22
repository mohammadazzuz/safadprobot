# Entry point to run the bot and dashboard
import os
import threading
from flask import Flask
from flask import Flask, redirect, url_for, render_template, request, session
from safadprobot.routes.dashboard import dashboard_bp
from safadprobot.routes.callback import callback
from safadprobot.auth.discord_oauth import exchange_code, get_login_url, get_user_data, get_user_guilds
from safadprobot.routes.out_oauth import out_oauth
from safadprobot.bot_instance import run_bot

# إنشاء تطبيق Flask
print("[INIT] Starting Flask app...")
app = Flask(__name__)

# تحميل المفتاح السري
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
print("[INIT] Loaded SECRET_KEY")

app.register_blueprint(callback)


# تسجيل البلوبريـنتس
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

print("[ROUTES] Dashboard blueprint registered.")

app.register_blueprint(out_oauth)


# تشغيل بوت ديسكورد في Thread منفصل
def start_bot():
    print("[BOT] Starting Discord bot...")
    run_bot()
    print("[BOT] Bot thread exited.")  # ما لازم توصل لهون إلا لو البوت وقف

bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
print("[BOT] Bot thread started.")



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return redirect(get_login_url())



print(app.url_map)

# تشغيل تطبيق Flask
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"[FLASK] Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port)