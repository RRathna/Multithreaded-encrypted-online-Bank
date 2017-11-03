drop table if exists customers
create table customers(id int primary key autoincrement,
acc_type varchar not null,
first_name varchar not null,
last_name varchar not null,
address varchar not null,
emailid Varchar not null,
password varchar not null,
phoneno varchar not null,
dob date not null,
securityq1 varchar not null,
securityq2 varchar not null);

drop table if exists account_details
create table account_details(acc_id integer primary key autoincrement not null,
  id int,primary key (acc_id),foreign key(id) references login(id) not null,
  trans_date date not null,
  transaction_id varchar not null,
  message varchar not null,
  amount varchar not null,
  from_to varchar not null,
  debit varchar,
  credit varchar,
  balance varchar not null);
