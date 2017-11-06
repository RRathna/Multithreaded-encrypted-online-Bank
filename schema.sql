drop database if exists Bank_DB;
create schema Bank_DB;
USE Bank_DB;
drop table if exists customers;
create table customers(id int not null primary key auto_increment,
first_name varchar(40) not null,
last_name varchar(40) not null,
address varchar(100) not null,
emailid Varchar(40) not null,
password varchar(100) not null,
phoneno varchar(20) not null,
ssn varchar(10) not null,
user_name varchar(20) not null);

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


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_user`(
  first_name varchar(40),
  last_name varchar(40),
  address varchar(100),
  emailid Varchar(40),
  password varchar(100),
  phoneno varchar(20),
  ssn varchar(10),
  user_name varchar(20)
)
/*select 'I am in stored procedure';*/
BEGIN
    if ( select exists(select 1 from customers where ssn = ssn)) THEN

        select 'Username Exists !!';

    ELSE

        insert into customers
        (
            first_name,
            last_name,
            address,
            emailid,
            password,
            phoneno,
            ssn,
            user_name

        )
        values
        (
          first_name,
          last_name,
          address,
          emailid,
          password,
          phoneno,
          ssn,
          user_name
        );

    END IF;
END$$
DELIMITER ;
