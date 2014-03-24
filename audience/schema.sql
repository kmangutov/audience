

drop table if exists entries;
drop table if exists users;
drop table if exists shares;

create table users (
	user_id	integer primary key autoincrement,
	user_login	text not null,
	user_pass	text not null
);

create table entries (
    entry_id	integer primary key autoincrement,
    entry_url	text not null
);

create table shares (
	share_id	integer primary key autoincrement,
	share_source	integer not null,
	share_value	integer not null,
	foreign key(share_source) references users(user_id),
	foreign key(share_value) references entries(entry_id)
);
