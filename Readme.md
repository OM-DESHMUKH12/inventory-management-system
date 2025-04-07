Please create your own database in mysql


<!-- create database inventory_db;
use inventory_db;

create table inventory (
	item_id int auto_increment primary key,
	name varchar(100) not null,
	quantity INT NOT NULL CHECK (quantity >= 0),
	price FLOAT NOT NULL CHECK (price >= 0),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table user (
	user_id int auto_increment primary key,
	username varchar(100) not null unique,
	email varchar(200) not null unique,
    password varchar(255) not null,
    created_at timestamp default current_timestamp
); -->

Run this command to create the db schema