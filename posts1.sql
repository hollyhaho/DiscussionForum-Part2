DROP TABLE IF EXISTS posts;

CREATE TABLE IF NOT EXISTS posts(
	post_Id INTEGER PRIMARY KEY ASC,
	post_text TEXT NOT NULL,
	post_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	post_authorId INTEGER,
	post_forumId INTEGER,
	post_threadId GUID);


insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('Why should I use Redis over other databases?','charlie', 4, '7f308475-f1e4-46b4-8914-df347d6884ef');
insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('It is a key-value database that has very quick access ability','bob', 4, '7f308475-f1e4-46b4-8914-df347d6884ef');
insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('When is a good time for me to use Redis?', 'charlie', 1, '417ef8c4-0bb1-450c-8bbb-e49b7656cbec');
