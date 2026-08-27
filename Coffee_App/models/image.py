def insert_images(cursor, post_id, image_urls):
    if not image_urls:
        return

    sql = """
        INSERT INTO images (
            post_id,
            image_url,
            display_order
        )
        VALUES (%s, %s, %s)
    """
    values = [
        (post_id, image_url, display_order)
        for display_order, image_url in enumerate(image_urls, start=1)
    ]
    cursor.executemany(sql, values)


def find_images_by_post_id(cursor, post_id):
    sql = """
        SELECT
            id,
            image_url,
            display_order
        FROM images
        WHERE post_id = %s
        ORDER BY display_order
    """
    cursor.execute(sql, (post_id,))
    return cursor.fetchall()


def find_images_by_post_ids(cursor, post_ids):
    if not post_ids:
        return []

    placeholders = ", ".join(["%s"] * len(post_ids))
    sql = f"""
        SELECT
            id,
            post_id,
            image_url,
            display_order
        FROM images
        WHERE post_id IN ({placeholders})
        ORDER BY post_id, display_order
    """
    cursor.execute(sql, tuple(post_ids))
    return cursor.fetchall()
