drop database NSRL;
create database NSRL;
use NSRL;
create Table uniq(id int not null auto_increment, SHA1 VARCHAR(255) not null, MD5 VARCHAR(255) not null,CRC32 VARCHAR(255) ,FileName VARCHAR(255) not null,FileSize VARCHAR(255) not null,ProductCode VARCHAR(255) not null,OpSystemCode VARCHAR(255) not null,SpecialCode VARCHAR(255), primary key (id));
load data local infile  [["location of your NSRLFile.txt"]] into table uniq fields terminated by "," lines terminated by "\n" ignore 1 rows (SHA1,MD5,CRC32,FileName,FileSize,ProductCode,OpSystemCode,SpecialCode);

create Table user(SHA1 VARCHAR(255) UNIQUE not null, vtstatus int not null default 0, primary key (SHA1));
