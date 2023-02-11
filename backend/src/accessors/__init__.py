from time import sleep
import psycopg2
import os

from flask import g

from shared.constants import WAIT_FOR_DB_IN_SECONDS


def is_db_ready():
    for i in range(WAIT_FOR_DB_IN_SECONDS):
        try:
            g.db = psycopg2.connect(
                host=os.environ["DB_HOST"],
                database=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
        except Exception as e:
            sleep(1)

    if g.db:
        print("DB Loaded")
        return

    raise Exception("Can't load DB")


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )

        # g.db.row_factory = psycopg2.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def _create_index(cursor, table_name, col_name):
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS"
        f" {table_name}_{col_name}_idx ON {table_name}"
        f" ({col_name});",
    )


def improve_db():
    db = get_db()
    with db.cursor() as cursor:
        _create_index(cursor, "regions", "parent_slug")
        _create_index(cursor, "ports", "parent_slug")
        _create_index(cursor, "prices", "day")
        _create_index(cursor, "prices", "orig_code")
        _create_index(cursor, "prices", "dest_code")
    db.commit()
