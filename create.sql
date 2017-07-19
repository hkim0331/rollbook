create table rollbook (
    id integer primary key auto_increment,
    user varchar(20) not null,
    date varchar(10) not null,
    hour integer not null,
    message text not null,
    utc datetime default CURRENT_TIMESTAMP);

create table assess (
  id integer primary key auto_increment,
  user varchar(20) not null,
  date varchar(10) not null,
  assess char(1) default ' ',
  utc datetime default CURRENT_TIMESTAMP);
