# Entry point to run the bot and dashboard
import os
import threading
from flask import Flask

from safadprobot.routes.dashboard import dashboard_bp
from safadprobot.routes.callback import callback_bp

from safadprobot.bot_instance import run_bot

# إنشاء تطبيق Flask
print("[INIT] Starting Flask app...")
app = Flask(__name__)

# تحميل المفتاح السري
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
print("[INIT] Loaded SECRET_KEY")

# تسجيل البلوبريـنتس
app.register_blueprint(dashboard_bp)
print("[ROUTES] Dashboard blueprint registered.")

app.register_blueprint(callback_bp)
print("[ROUTES] Callback blueprint registered.")

# تهيئة قاعدة البيانات
#print("[DB] Initializing database...")
#init_db()
#print("[DB] Database initialized.")

# تشغيل بوت ديسكورد في Thread منفصل
def start_bot():
    print("[BOT] Starting Discord bot...")
    run_bot()
    print("[BOT] Bot thread exited.")  # ما لازم توصل لهون إلا لو البوت وقف

bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
print("[BOT] Bot thread started.")

# تشغيل تطبيق Flask
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"[FLASK] Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port)