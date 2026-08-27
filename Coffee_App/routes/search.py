from flask import Blueprint, request, render_template
from Coffee_App.models.category import get_categories
from Coffee_App.models.post import search_posts

search_bp = Blueprint("search", __name__)


# 検索画面の表示
@search_bp.route("/search")
def search_page():
    keyword = request.args.get("keyword", "")
    category = request.args.get("category", "")

    if keyword or category:
        posts = search_posts(keyword, category)
        return render_template(
            "search/search_results.html",
            keyword=keyword,
            category=category,
            posts=posts,
        )

    categories = get_categories()

    return render_template(
        "search/search.html",
        categories=categories,
    )

@search_bp.get("/search/page")
def search_page():
    return render_template("search/search.html")
