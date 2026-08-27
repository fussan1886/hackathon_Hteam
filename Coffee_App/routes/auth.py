from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from Coffee_App.models.user import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth-test")
def auth_test():
    return "Auth route is working!"


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    # 必須項目チェック
    if not username or not email or not password:
        return {
            "message": "username, email, password are required"
        }, 400

    try:
        # メールアドレスの重複チェック
        existing_user = User.find_by_email(email)

        if existing_user:
            return {
                "message": "This email is already registered."
            }, 409

        # パスワードをハッシュ化
        password_hash = generate_password_hash(password)

        # ユーザー登録
        User.create(
            username,
            email,
            password_hash
        )

        return redirect(url_for("auth.login"))

    except Exception as e:
        return {
            "message": f"User registration failed: {e}"
        }, 500

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    # 必須項目チェック
    if not email or not password:
        return {
            "message": "email and password are required."
        }, 400

    try:
        # メールアドレスからユーザーを検索
        user = User.find_active_by_email(email)

        # ユーザーが存在しない
        if not user:
            return {
                "message": "Invalid email or password."
            }, 401

        # パスワードが一致しない
        if not check_password_hash(
            user["password_hash"],
            password
        ):
            return {
                "message": "Invalid email or password."
            }, 401

        # ログイン状態をSessionに保存
        session["user_id"] = user["id"]

        # ログイン成功後はタイムラインへ移動
        return redirect(url_for("posts.timeline"))

    except Exception as e:
        return {
            "message": f"Login failed: {e}"
        }, 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return {
        "message": "Logout successful!"
    }, 200
