import sqlite3

from flask import g

def sql_init():
    if not "db" in g:
        g.db = sqlite3.connect("../database.db")
        g.cursor = g.db.cursor()

def sql_close():
    sql_init()
    db = g.pop("db", None)

    if db is not None:
        db.close()

def sql_commit():
    sql_init()
    g.db.commit()

def sql_rollback():
    sql_init()
    g.db.rollback()

def sql_execute(*args):
    sql_init()
    g.cursor.execute(*args)
    return g.cursor
