# webapp-discussionforum

Use Flask to create a Web Service API for a discussion forum application.

To run program, make sure you install flask and BasicAuth:
```
pip3 install flask
pip3 install Flask-BasicAuth
```
To initialize the database doing the following:
```
export FLASK_APP=discussion_api
flask init_db
```


# API Calls

### 1. GET /forums
Curl call:
```
curl localhost:5000/forums
```
Response: Success 200 OK
```
[
	
	{
		"Id": 1,
		"forum_creator": "alice",
		"forum_name": "redis"
	},
	{
		"Id": 2,
		"forum_creator": "bob",
		"forum_name": "mongodb"
	},
	{
		"Id": 3,
		"forum_creator": "bob",
		"forum_name": "python"
	},
	{
		"Id": 4,
		"forum_creator": "bob",
		"forum_name": "flask"
	}
]
```

### 2. POST /forums
Curl call: 
```
curl -v -u holly:password -d '{"forum_name":"HTML"}' -H "Content-Type: application/json" -X POST localhost:5000/forums
```

+ Error: 409 for duplicate forum names
+ Success: 201 forum created

### 3.  GET /forums/<forum_id>
Curl call: 
```
curl localhost:5000/forums/1
```
+ Response: Success 200 OK
+ Curl call: 
```
[
  {
    "Id": "e8c3c68f-4557-450d-a4ad-f3d20cb50c10",
    "creator": "bob",
    "timestamp": "Sun, 28 Oct 2018 03:01:32 GMT",
    "title": "Does anyone know how to start Redis?!!!!"
  },
  {
    "Id": "417ef8c4-0bb1-450c-8bbb-e49b7656cbec",
    "creator": "charlie",
    "timestamp": "Sun, 28 Oct 2018 03:01:32 GMT",
    "title": "When is a good time for me to use Redis?"
  }
]
```
### 4.  POST /forums/<forum_id>
Curl call: 
```
curl -v -u holly:password -d '{"thread_title":"Do you love Redis?", "text": "I love it very much"}' -H "Content-Type: application/json" -X POST localhost:5000/forums/1
```

+ Successful Response: 201 Created
+ Sucess: Thread and Post Created
+ Error: 404 Not Found

### 5.  GET /forums/<forum_id>/<thread_id>
Curl call: 
```
curl localhost:5000/forums/1/e8c3c68f-4557-450d-a4ad-f3d20cb50c10
```
+ Response: Success 200 OK
+ Curl call: 
```
[
  {
    "author": "bob",
    "text": "I am having trouble connecting to Redis. Do you have any idea how to do it?",
    "timestamp": "Sun, 28 Oct 2018 03:01:32 GMT"
  },
  {
    "author": "alice",
    "text": "I Think you can google it",    
    "timestamp": "Sun, 28 Oct 2018 03:01:32 GMT"
  }
]
```
### 6. POST /forums/<forum_id>/<thread_id>
Curl call: 
```
curl -v -u holly:password -d '{"text":"You can go stackoverflow and post your question"}' -H "Content-Type: application/json" -X POST localhost:5000/forums/1/e8c3c68f-4557-450d-a4ad-f3d20cb50c10
```

+ Successful Response: 201 Created
+ Sucess: Post Created
+ Error: 404 Not Found

### 7.  POST /users
Curl call: 
```
curl -v -d '{"username": "dungho", "password": "whatisthat"}' -H "Content-Type: application/json" -X POST localhost:5000/users
```

+ Successful Response: 201 Created
+ Sucess: Account Created
+ Error: 404 Not Found

### 8. PUT /users/<username>
Curl call: 
```
curl -v -u holly:password -d '{"password":"newpassword"}' -H "Content-Type: application/json" -X PUT localhost:5000/users/holly
```

+ Successful Response: 201 Created
+ Sucess: User password Changed
+ Error: 404 Not Found Username does not exist.
+ Error 2: 409 Conflict Username does not match the current authenticated user
