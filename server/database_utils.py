"""Some utilities for connecting to the database."""

import sqlite3
import os
import traceback


def database_name():
    """Get the name of the database."""
    return "mudima.db"


def database_path(name):
    """Get the path of the database."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), name)


class DatabaseConnection:
    """Handle the connection to the database."""

    def __init__(self, path=None, refresh=False):
        db_path = database_path(path if path else database_name())
        exists = os.path.exists(db_path)
        if exists and refresh:
            os.remove(db_path)
            exists = False
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        if not exists:
            self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE topic (name TEXT, id TEXT PRIMARY KEY, image_url TEXT,
                               category TEXT, fit_x DOUBLE, fit_y DOUBLE)""")
        self.cursor.execute("""CREATE TABLE article (name TEXT, link TEXT PRIMARY KEY, image_url TEXT,
                               article_text TEXT, topic_id TEXT, date DATETIME,
                               fit_x DOUBLE, fit_y DOUBLE, group_fit_x DOUBLE, group_fit_y DOUBLE,
                               popularity UNSIGNED INT DEFAULT 1, source TEXT, favicon TEXT,
                               FOREIGN KEY(topic_id) REFERENCES topic(id) ON DELETE CASCADE)""")
        self.cursor.execute("CREATE TABLE bad_article (link TEXT PRIMARY KEY)")
        self.cursor.execute("CREATE TABLE keyword (keyword TEXT, article_link TEXT, "
                            "FOREIGN KEY(article_link) REFERENCES article(link) ON DELETE CASCADE)")
        self.connection.commit()

    def __enter__(self):
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        except IOError:
            traceback.print_exc()
        self.connection.close()
