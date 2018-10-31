DROP TABLE IF EXISTS posts;

CREATE TABLE IF NOT EXISTS posts(
	post_Id INTEGER PRIMARY KEY ASC,
	post_text TEXT NOT NULL,
	post_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	post_authorId INTEGER,
	post_forumId INTEGER,
	post_threadId GUID);

insert into posts (post_text, post_authorid, post_forumid, post_threadId) values('Why should I use mongodb over cassandra?', 'charlie', 2, 'ec93faf8-1bb7-4c3a-aa39-c8d6e909e93d');
insert into posts (post_text, post_authorid, post_forumid, post_threadId) values('It is a matter of architecture choice', 'holly', 2, 'ec93faf8-1bb7-4c3a-aa39-c8d6e909e93d');

