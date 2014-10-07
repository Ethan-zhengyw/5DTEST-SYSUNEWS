/*grant all privileges on sysunewsDB.* to sysunews@localhost identified by 'sysunews';*/

create database if not exists sysunews;

use sysunews;

/*create table teacher_table

(

teacher_id int auto_increment,

teacher_name varchar(255),

primary key(teacher_id)

);
*/

drop table urls;
create table if not exists urls 
(
    newsid int,
    module int,
    url varchar(50),
    PRIMARY KEY (newsid)
)default charset=utf8;

drop table news;
create table if not exists news
(
    newsid int,
    module int,
    visit_times int,
    date varchar(10),
    url varchar(100),
    imgs varchar(2000),
    author varchar(50),
    editor varchar(50),
    h1 varchar(100),
    h2 varchar(100),
    source varchar(50),
    maindiv varchar(15000),
    PRIMARY KEY (newsid)
)default charset=utf8;
