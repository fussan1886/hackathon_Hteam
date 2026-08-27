from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, render_template, request, session

from Coffee_App.database import get_db
from Coffee_App.models.image import find_images_by_post_id, insert_images
from Coffee_App.models.post import delete_post, find_post_by_id, find_posts, insert_post


posts_bp = Blueprint("posts", __name__)


def _is_allowed_image(filename):
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def _serialize_post(post, images):
    return {
        "id": post["id"],
        "user_id": post["user_id"],
        "content": post["content"],
        "visibility": post["visibility"],
        "images": images,
        "created_at": post["created_at"].isoformat(),
        "updated_at": post["updated_at"].isoformat(),
    }


@posts_bp.get("/posts/create")
def post_create():
    return render_template("posts/post_create.html")

@posts_bp.get("/posts/timeline")
def timeline():
    return render_template("posts/timeline.html")

@posts_bp.post("/posts")
def create_post():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "ログインが必要です。"}), 401

    content = request.form.get("content", "").strip()
    if not content:
        return jsonify({"error": "本文は必須です。"}), 400

    image_files = [image for image in request.files.getlist("images") if image.filename]
    invalid_files = [image.filename for image in image_files if not _is_allowed_image(image.filename)]
    if invalid_files:
        return jsonify({"error": "サポートされていない画像フォーマットです。", "files": invalid_files}), 400

    upload_directory = Path(current_app.config["POST_UPLOAD_FOLDER"])
    upload_directory.mkdir(parents=True, exist_ok=True)
    saved_files = []
    image_urls = []
    connection = None

    try:
        for image_file in image_files:
            extension = Path(image_file.filename).suffix.lower()
            stored_name = f"{uuid4().hex}{extension}"
            image_file.save(upload_directory / stored_name)
            saved_files.append(upload_directory / stored_name)
            image_urls.append(f"/static/uploads/posts/{stored_name}")

        connection = get_db()
        with connection.cursor() as cursor:
            post_id = insert_post(
                cursor,
                user_id=user_id,
                content=content,
            )
            insert_images(cursor, post_id, image_urls)
            post = find_post_by_id(cursor, post_id)
            images = find_images_by_post_id(cursor, post_id)

        connection.commit()
    except Exception:
        if connection is not None:
            connection.rollback()
        for saved_file in saved_files:
            saved_file.unlink(missing_ok=True)
        current_app.logger.exception("投稿の作成に失敗しました。")
        return jsonify({"error": "投稿の作成に失敗しました。"}), 500

    return jsonify(_serialize_post(post, images)), 201


@posts_bp.get("/posts")
def get_posts():
    connection = get_db()
    with connection.cursor() as cursor:
        posts = find_posts(cursor)
        result = [
            _serialize_post(post, find_images_by_post_id(cursor, post["id"]))
            for post in posts
        ]

    return jsonify(result), 200


@posts_bp.get("/posts/<int:post_id>")
def get_post(post_id):
    try:
        connection = get_db()
        with connection.cursor() as cursor:
            post = find_post_by_id(cursor, post_id)
            if post is None:
                return jsonify({"error": "投稿が見つかりません。"}), 404
            images = find_images_by_post_id(cursor, post_id)
    except Exception:
        current_app.logger.exception("投稿の取得に失敗しました。")
        return jsonify({"error": "投稿の取得に失敗しました。"}), 500

    return jsonify(_serialize_post(post, images)), 200


@posts_bp.route("/posts/<int:post_id>", methods=["DELETE", "POST"])
def post_delete(post_id):
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "ログインが必要です。"}), 401

    connection = get_db()
    with connection.cursor() as cursor:
        post = find_post_by_id(cursor, post_id)
        if post is None:
            return jsonify({"error": "投稿が見つかりません。"}), 404
        if post["user_id"] != user_id:
            return jsonify({"error": "この投稿は削除できません。"}), 403
        delete_post(cursor, post_id)
    connection.commit()

    return jsonify({"message": "投稿を削除しました。"}), 200

