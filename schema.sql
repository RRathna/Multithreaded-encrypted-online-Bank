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
user_name varchar(20) not null,
UNIQUE(user_name),
UNIQUE(ssn));

drop table if exists account_details;
create table account_details(acc_id int not null primary key,
  user_id int not null,
  acc_type varchar(10) not null,
  balance int not null,
  date_created date not null,
  FOREIGN KEY (user_id) references customers(id));

drop table if exists transactions;
create table transactions(trans_id int not null primary key,
  acc_id int not null,
  trans_type varchar(10) not null,
  amount int not null,
  trans_party_acc int not null,
  trans_date date not null,
  transaction_Approval varchar(20) not null,
  foreign key (acc_id) references account_details(acc_id));

drop table if exists roles;
create table roles(role_key int not null primary key auto_increment,
  user_id int not null,
  role varchar(20) not null,
  foreign key (user_id) references customers(id));


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_user`(
  IN first_name varchar(40),
  IN last_name varchar(40),
  IN address varchar(100),
  IN emailid Varchar(40),
  IN password varchar(100),
  IN phoneno varchar(20),
  IN u_name varchar(20)
)
/*select 'I am in stored procedure';*/
BEGIN
    /*if ((select 1 from customers where ssn = ssn)) THEN*/
    IF not EXISTS(select * from customers where (user_name = u_name)) THEN
        insert into customers
        (
            first_name,
            last_name,
            address,
            emailid,
            password,
            phoneno,
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
          u_name
        );
    ELSE
        select 'User Exists !!';
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_account`(
  IN u_id int,
  IN ac_type varchar(10),
  IN bal int
)
  BEGIN
      if exists(select 1 from customers where id = u_id) THEN
        SET @ranum = (SELECT FLOOR(RAND() * 9999) AS random_num FROM account_details WHERE "random_num" NOT IN (SELECT acc_id FROM account_details) LIMIT 1);
        IF (@ranum IS NULL) THEN
          SET @ranum = (FLOOR(RAND() * 9999));
          end IF;
        insert into account_details
        (
          acc_id,
          user_id,
          acc_type,
          balance,
          date_created
        )
        values
        (
          @ranum,
          u_id,
          ac_type,
          bal,
          CURDATE()
        );
      else
        select 'User does not exists to create account';
      end if;
  END$$
  DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_teller`(
    IN u_id int)
     BEGIN
      if not exists(select * from roles where (user_id = u_id and role = 'teller')) THEN
        insert into roles
          (
            user_id,
            role
          )
        values
          (
            u_id,
            'teller'
          );
      else
        select 'Teller with this ID already exists';
      end if;
    END$$
    DELIMITER ;

    DELIMITER $$
    CREATE DEFINER=`root`@`localhost` PROCEDURE `create_admin`(
        IN u_id int)
         BEGIN
          if not exists(select * from roles where (user_id = u_id and role = 'admin')) THEN
            insert into roles
              (
                user_id,
                role
              )
            values
              (
                u_id,
                'admin'
              );
          else
            select 'Admin with this ID already exists';
          end if;
        END$$
        DELIMITER ;
