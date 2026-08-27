from flask import Blueprint, abort, render_template, request

from Coffee_App.models.user import User


users_bp = Blueprint("users", __name__)


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = User.find_by_id(user_id)

    if not user:
        abort(404)

    return render_template("users/profile.html", user=user)

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    username = data.get("username")
    profile_text = data.get("profile_text")

    print("profile_text:", profile_text, flush=True)
    # 必須チェック
    if not username:
        return {
            "message": "username is required."
        }, 400

    # ユーザーが存在するか確認
    user = User.find_by_id(user_id)

    if not user:
        return {
            "message": "User not found."
        }, 404

    try:
        User.update(
            user_id,
            username,
            profile_text
        )

        return {
            "message": "User updated successfully!"
        }, 200

    except Exception as e:
        return {
            "message": f"User update failed: {e}"
        }, 500

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = User.find_by_id(user_id)

    if not user:
        return {
            "message": "User not found."
        }, 404

    try:
        User.delete(user_id)

        return {
            "message": "User deleted successfully!"
        }, 200

    except Exception as e:
        return {
            "message": f"User deletion failed: {e}"
        }, 500
