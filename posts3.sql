DROP TABLE IF EXISTS posts;

CREATE TABLE IF NOT EXISTS posts(
	post_Id INTEGER PRIMARY KEY ASC,
	post_text TEXT NOT NULL,
	post_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	post_authorId INTEGER,
	post_forumId INTEGER,
	post_threadId GUID);


insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('I am having trouble connecting to Redis. Do you have any idea how to do it?','bob', 1, 'e8c3c68f-4557-450d-a4ad-f3d20cb50c10');
insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('I Think you can google it', 'alice', 1, 'e8c3c68f-4557-450d-a4ad-f3d20cb50c10');
insert into posts (post_text, post_authorid, post_forumid, post_threadId) values ('I want to use Edis for a project. Is it a good idea to use it for back end development?','holly', 1, '417ef8c4-0bb1-450c-8bbb-e49b7656cbec');

