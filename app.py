import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, jsonify

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)

# connect to the database
def connect_db():
    """Connects to the database"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def show_entries():
    """Search the database for entries, then displays them"""
    db = get_db()
    cur = db.execute('select * from entries order id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

# close the database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    init_db()
    app.run()
