import flask
from flask import request, jsonify, render_template, json, abort, Response, flash, g, current_app, make_response
from flask_basicauth import BasicAuth
import sqlite3
import uuid

app = flask.Flask(__name__)
app.config['DEBUG'] = True

DATABASES = ['./init.db', './post1.db', './post2.db', './post3.db']
SQL = ['init.sql', 'posts1.sql', 'posts2.sql', 'posts3.sql']

class Authentication(BasicAuth):
    def check_credentials(self, username, password):
        print('check_credentials')
        # query from database 
        query = "SELECT * from users where username ='{}'".format(username)
        db_index = 0
        user = query_db(query, db_index)
        if user == []:
            return False
        if user[0]['password'] == password:
            current_app.config['BASIC_AUTH_USERNAME'] = username
            current_app.config['BASIC_AUTH_PASSWORD'] = password
            return True
        else: 
            return False

basic_auth = Authentication(app)

#Function Connect Database
def get_db(db_index):
    database_name = '_database' + str(db_index)
    db = getattr(g, database_name, None)
    print(DATABASES[db_index])

    if db is None:
        db = g._database = sqlite3.connect(DATABASES[db_index])

    return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Function  execute script
def init_db():
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))
    with app.app_context():
        for i in range(0, 4):
            db = get_db(i)
            print(db)
            with app.open_resource(SQL[i], mode='r') as f:
                print(SQL[i])
                db.cursor().executescript(f.read())
            db.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#Function using for query database
#Fetch each data one by one based on the query provided
def query_db(query, db_index, args=(), one=False):
    print(db_index)
    conn = get_db(db_index)
    conn.row_factory = dict_factory
    cur = conn. cursor()
    fetch = cur.execute(query).fetchall()
    return fetch


# Function that formats the date
def getTimeStamp(threadOrPost):
    timeType = ''
    if threadOrPost == 'thread':
        timeType = 'thread_time'
    else:
        timeType = 'post_time'
    # timestamp = "strftime('%m', datetime(thread_time, 'unixepoch')) as month"
    timestampDay = '''case cast (strftime('%w', {}) as integer)
        when 0 then 'Sun, '
        when 1 then 'Mon, '
        when 2 then 'Tues, '
        when 3 then 'Wed, '
        when 4 then 'Thurs, '
        when 5 then 'Fri, '
        else 'Sat, ' end'''.format(timeType)
    timestampDate = "strftime('%d', {})".format(timeType)
    timestampMonth = '''case cast(strftime('%m', {}) as integer)
        when 1 then ' Jan ' 
        when 2 then ' Feb '
        when 3 then ' Mar '
        when 4 then ' Apr '
        when 5 then ' May '
        when 6 then ' Jun '
        when 7 then ' July '
        when 8 then ' Aug '
        when 9 then ' Sept '
        when 10 then ' Oct '
        when 11 then ' Nov '
        when 12 then ' Dec ' 
        else '' end'''.format(timeType)
    timestampYear = "strftime('%Y', {})".format(timeType)
    timestampTime = "strftime('%H:%M:%S', {})".format(timeType)
    timestamp = '''{} || {} || {} || {} || ' ' ||  {} || ' ' ||'GMT' '''.format(timestampDay, timestampDate, timestampMonth, timestampYear, timestampTime)
    return timestamp

def get_server_id(user_id):
    '''return sharding for server'''
    
    return int(user_id) % 3 + 1

@app.route('/forums', methods = ['GET'])
def api_forums():
    query = "SELECT * FROM forums;"
    # db_index is 0 bc we want to go to init.db
    db_index = 0
    forums = query_db(query, db_index)

    return jsonify(forums)

#POST FORUM
@app.route('/forums', methods=['POST'])
@basic_auth.required
def post_forums():

    data = request.get_json(force=True)
    name = data['forum_name']

    creator = current_app.config['BASIC_AUTH_USERNAME']
    query = 'SELECT forum_name FROM forums'
    db_index = 0
    forum_names = query_db(query, db_index)
    for forum_name in forum_names:
        if forum_name['forum_name'] == name:
            error = '409 A forum already exists with the name ' + name
            return make_response(jsonify({'error': error}), 409)
   
    db = get_db(db_index)
    db.execute('insert into forums (forum_name, forum_creator) values (?, ?)',(name, creator))
    db.commit()

    query = "select Id from forums where forum_name ='{}'".format(name)
    new_forum = query_db(query, db_index)
    response = make_response('Success: forum created')
    response.headers['location'] = '/forums/{}'.format(new_forum[0]['Id'])
    response.status_code = 201

    return response

#List threads in the specified forum
@app.route('/forums/<int:forum_id>', methods = ['GET'])
def api_threads(forum_id):
    query = 'SELECT Id FROM forums WHERE Id = ' + str(forum_id) +';'
    db_index = 0
    forum = query_db(query, db_index)
    if not forum :
        error = '404 No forum exists with the forum id of ' + str(forum_id)
        return make_response(jsonify({'error': error}), 404)
    else:
        
        timestamp = getTimeStamp('thread')
        query = 'SELECT Id, thread_creator as creator, {} as timestamp, thread_title as title FROM threads WHERE forum_id = {} ORDER BY thread_time DESC'.format(timestamp,str(forum_id))
        threads = query_db(query, db_index)
        return jsonify(threads)


#POST THREAD
@app.route('/forums/<int:forum_id>', methods=['POST'])
@basic_auth.required
def post_thread(forum_id):

    data = request.get_json(force=True)
    title = data['thread_title']
    text = data['text']
    thread_id = uuid.uuid4()
    creator = current_app.config['BASIC_AUTH_USERNAME']
    

     # Select from forums on forum id to make sure that the forum exists
    query = 'SELECT * FROM forums WHERE id = ' + str(forum_id)
    db_index = 0
    forum = query_db(query, db_index)
    print(forum)
    if len(forum) == 0:
        error = '404 No forum exists with the forum id of ' + str(forum_id)
        return make_response(jsonify({'error': error}), 404)
    # If forum exist, insert into threads table
    db = get_db(db_index)
    db.execute('insert into threads (Id, thread_title, thread_creator, forum_Id) values (?, ?, ?, ?)',(str(thread_id), title, creator, str(forum_id)))
    db.commit()
 
    print(thread_id)
    print(get_server_id(thread_id))
    post_server_id = get_server_id(thread_id)
    db = get_db(post_server_id)
    # Insert text as a new post
    db.execute('insert into posts (post_text, post_authorid , post_threadId, post_forumid) values (?, ?, ?, ?)',(text, creator, str(thread_id), str(forum_id)))
    db.commit()

    response = make_response("Success: Thread and Post created")
    response.headers['location'] = '/forums/{}/{}'.format(str(forum_id), str(thread_id))
    response.status_code = 201
    return response

if __name__ == "__main__":
    app.run(debug=True)