use dinners;
create table image_metadata
(

id Integer primary key NOT NULL AUTO_INCREMENT,
name_tag  varchar(255),
image_path	varchar(255),
image_name varchar(255),
recipe     text,
created_at timestamp


);

CREATE TABLE users (
     id integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `username` varchar(255),
    `password` varchar(255),
    `full_name` varchar(255),
    `email_address` varchar(255),
	 created_at timestamp

    
);


CREATE TABLE favourite_dinners (
    `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `image_id` int,
    `user_id` int,
    selected_at timestamp
);
