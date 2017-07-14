create table rollbook (
    id integer primary key auto_increment,
    user varchar(20) not null,
    date varchar(10) not null,
    hour integer not null,
    message text not null,
    timestamp datetime default CURRENT_TIMESTAMP);


