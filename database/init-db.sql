create database if not exists ece140;

use ece140;

-- DUMP EVERYTHING... YOU REALLY SHOULDN'T DO THIS!
drop table if exists users;

create table if not exists users (
  id         integer auto_increment primary key,
  first_name varchar(30) not null,
  last_name  varchar(30) not null,
  created_at timestamp
);

insert into users (first_name, last_name, created_at) values
  ("Zendaya", "", current_timestamp),
  ("Tom", "Holland", current_timestamp),
  ("Tobey", "Maguire", current_timestamp),
  ("Andrew", "Garfield", current_timestamp)
;