import flask
from flask import request, jsonify, render_template, json, abort, Response, flash, g, current_app, make_response
import sqlite3
app = flask.Flask(__name__)
app.config['DEBUG'] = True
DATABASE = './init.db'
DATABASE_POSTS1 = "./posts1.db"
DATABASES = ['./init.db', './post1.db']
SQL = ['init.sql', 'posts1.sql']

#Function Connect Database
def get_db(db_index):
    database_name = '_database' + str(db_index)
    db = getattr(g, database_name, None)
    print('in get_db')
    print(DATABASES[db_index])

    if db is None:
        if db_index == 0:
            db = g._database = sqlite3.connect(DATABASES[db_index], detect_types=sqlite3.PARSE_DECLTYPES)
            print(db)
        elif db_index == 1:
            db = g._database = sqlite3.connect(DATABASES[db_index], detect_types=sqlite3.PARSE_DECLTYPES)

    return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    # db = g.pop('_database', None)
    # if db is not None:
    #     db.close()
#Function  execute script
def init_db():
    print('in init_db')
    with app.app_context():
        for i in range(0, 2):
            db = get_db(i)
            print(db)
            with app.open_resource(SQL[i], mode='r') as f:
                print(SQL[i])
                db.cursor().executescript(f.read())
            db.commit()
            # db.close()