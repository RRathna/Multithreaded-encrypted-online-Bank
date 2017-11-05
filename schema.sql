drop database if exists Bank_DB;
create schema Bank_DB;
USE Bank_DB;
drop table if exists customers;
create table customers(id int not null primary key auto_increment,
first_name varchar(40) not null,
last_name varchar(40) not null,
address varchar(100) not null,
emailid Varchar(40) not null,
password varchar(40) not null,
phoneno varchar(20) not null,
ssn varchar(10) not null,
dob date not null);

drop table if exists account_details;
create table account_details(acc_id int not null primary key auto_increment,
  user_id int not null,
  acc_type varchar(10) not null,
  balance int not null,
  date_created date not null,
  FOREIGN KEY (user_id) references customers(id));

drop table if exists transactions;
create table transactions(trans_id int not null primary key auto_increment,
  acc_id int not null,
  trans_type varchar(10) not null,
  amount int not null,
  trans_party_acc int not null,
  trans_date date not null,
  foreign key (acc_id) references account_details(acc_id));

drop table if exists roles;
create table roles(role_key int not null primary key auto_increment,
  user_id int not null,
  role varchar(20) not null,
  foreign key (user_id) references customers(id));
