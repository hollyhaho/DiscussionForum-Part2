DROP TABLE IF EXISTS posts;

CREATE TABLE IF NOT EXISTS posts(
	post_Id INTEGER PRIMARY KEY ASC,
	post_text TEXT NOT NULL,
	post_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	post_authorId INTEGER,
	post_forumId INTEGER,
	post_threadId GUID);

insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('Does anyone know how to start Redis?!!!!','bob', 1, 'e8c3c68f-4557-450d-a4ad-f3d20cb50c10');
insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('I Think you can google it', 'alice', 1, 'e8c3c68f-4557-450d-a4ad-f3d20cb50c10');


