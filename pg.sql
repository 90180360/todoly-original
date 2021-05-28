CREATE TABLE users (
	id SERIAL NOT NULL PRIMARY KEY, 
	username VARCHAR(20) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(500) NOT NULL, 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE todos (
	id SERIAL NOT NULL PRIMARY KEY, 
	title VARCHAR(50) NOT NULL, 
	"desc" VARCHAR(200), 
	status BOOLEAN NOT NULL, 
	user_id INTEGER NOT NULL REFERENCES users (id)
);