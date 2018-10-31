DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS threads;

CREATE TABLE  IF NOT EXISTS users(
	Id INTEGER PRIMARY KEY ASC, 
	username TEXT, 
	password TEXT
);

CREATE TABLE IF NOT EXISTS forums(
	Id INTEGER PRIMARY KEY ASC, 
	forum_name TEXT, 
	forum_creator TEXT,
	FOREIGN KEY (forum_creator) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS threads(
	Id GUID PRIMARY KEY,
	thread_title TEXT NOT NULL,
	thread_creator TEXT,
	thread_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	forum_Id INTEGER,
	FOREIGN KEY (forum_Id) REFERENCES forums(Id),
	FOREIGN KEY (thread_creator) REFERENCES users(username)
);


insert into threads (Id, thread_title, thread_creator, forum_id) values ('e8c3c68f-4557-450d-a4ad-f3d20cb50c10', 'Does anyone know how to start Redis?!!!!', 'bob', 1);
insert into threads (Id, thread_title, thread_creator, forum_id) values ('417ef8c4-0bb1-450c-8bbb-e49b7656cbec', 'When is a good time for me to use Redis?', 'charlie', 1);
insert into threads (Id, thread_title, thread_creator, forum_id) values ('ec93faf8-1bb7-4c3a-aa39-c8d6e909e93d', 'Why should I use mongodb over cassandra?', 'charlie', 2);
insert into threads (Id, thread_title, thread_creator, forum_id) values ('7f308475-f1e4-46b4-8914-df347d6884ef', 'Why should I use Redis over other databases?', 'charlie', 4);

insert into forums (forum_name, forum_creator) values ('redis', 'alice');
insert into forums (forum_name, forum_creator) values ('mongodb', 'bob');
insert into forums (forum_name, forum_creator) values ('python', 'bob');
insert into forums (forum_name, forum_creator) values ('flask', 'bob');

insert into users (username, password) values ('holly', 'password');
insert into users (username, password) values ('nguyen', 'password');
insert into users (username, password) values ('bob', 'password');
insert into users (username, password) values ('alice', 'password');
insert into users (username, password) values ('bob', 'password');
insert into users (username, password) values ('charlie', 'password');