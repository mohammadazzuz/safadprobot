from flask import Blueprint, session, redirect, url_for

out_oauth = Blueprint('out_oauth', __name__)

@out_oauth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))  # أو أي مسار تريد إعادة التوجيه إليه بعد الخروج
