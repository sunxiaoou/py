use finance;
drop table if exists `instant_price`;
SET character_set_client = utf8mb4;
CREATE TABLE `instant_price` (
    `code` varchar(10) not null,
    `name` varchar(20) not null, 
    `ts` timestamp not null,
    `price` float not null,
    `pc` float not null,
    PRIMARY KEY (`code`,`ts`)
) engine = innodb default charset = utf8mb4;

-- alter table instant_price rename to instant2;
-- create table instant_price like instant2;
-- insert into instant_price select distinct * from instant2;
