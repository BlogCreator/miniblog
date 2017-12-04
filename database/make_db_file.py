import sqlite3
import os
from database import create_table

def create_database():
    if not os.path.exists(__file__+'/database.db'):
        db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"/database.db")
        var = filter(lambda it:not it.startswith('__'),dir(create_table))
        for i in var:
            db.execute(getattr(create_table,i))
        db.execute('PRAGMA foreign_keys = "1"')
        db.commit()
        db.close()
