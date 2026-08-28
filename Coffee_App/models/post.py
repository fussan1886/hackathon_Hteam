def insert_post(cursor, user_id, content, category_id):
    sql = """
        INSERT INTO posts (
            user_id,
            category_id,
            content,
            visibility
        )
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (user_id, category_id, content, "public"))
    return cursor.lastrowid


def find_post_by_id(cursor, post_id):
    sql = """
        SELECT
            id,
            user_id,
            content,
            visibility,
            created_at,
            updated_at
        FROM posts
        WHERE id = %s
        AND deleted_at IS NULL
    """
    cursor.execute(sql, (post_id,))
    return cursor.fetchone()


def find_posts(cursor):
    cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.content,
            p.visibility,
            p.created_at,
            p.updated_at,
            u.username,
            u.profile_image_url,
            (
                SELECT COUNT(*)
                FROM comments AS c
                WHERE c.post_id = p.id
            ) AS comment_count,
            (
                SELECT COUNT(*)
                FROM reactions AS r
                WHERE r.post_id = p.id
            ) AS reaction_count
        FROM posts AS p
        INNER JOIN users AS u ON u.id = p.user_id
        WHERE p.deleted_at IS NULL
          AND p.visibility = 'public'
          AND u.deleted_at IS NULL
        ORDER BY p.created_at DESC, p.id DESC
        LIMIT 100
        """)
    return cursor.fetchall()


def delete_post(cursor, post_id):
    cursor.execute(
        "UPDATE posts SET deleted_at = CURRENT_TIMESTAMP(6) WHERE id = %s",
        (post_id,),
    )


def search_posts(cursor, keyword, category_id=None):
    sql = """
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            c.category_name,
            p.content,
            p.visibility,
            p.created_at,
            p.updated_at,
            u.username,
            u.profile_image_url,
            (
                SELECT COUNT(*)
                FROM comments AS co
                WHERE co.post_id = p.id
            ) AS comment_count,
            (
                SELECT COUNT(*)
                FROM reactions AS r
                WHERE r.post_id = p.id
            ) AS reaction_count
        FROM posts AS p
        INNER JOIN users AS u ON u.id = p.user_id
        INNER JOIN categories AS c ON c.id = p.category_id
        WHERE p.deleted_at IS NULL
        AND p.visibility = 'public'
        AND u.deleted_at IS NULL
        AND p.content LIKE %s
        """

    params = [f"%{keyword}%"]

    if category_id:
        sql += """
        AND p.category_id = %s
        """

        params.append(category_id)

    sql += """
        ORDER BY p.created_at DESC, p.id DESC
        LIMIT 100
    """

    cursor.execute(sql, params)
    return cursor.fetchall()
