create table image_metadata
(

id Integer primary key,
name_tag  STRING,
image_path	STRING,
image_name STRING,
created_at timestamp


);

CREATE TABLE users (
     id integer PRIMARY KEY,
    `username` varchar(255),
    `password` varchar(255),
    `full_name` varchar(255),
    `email_address` varchar(255),
	 created_at timestamp

    
);


CREATE TABLE favourite_dinners (
    `id` integer PRIMARY KEY,
    `image_id` int,
    `user_id` int,
    selected_at timestamp
);
