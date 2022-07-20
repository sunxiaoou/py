use finance;
drop table if exists `instant_price`;
SET character_set_client = utf8mb4;
CREATE TABLE `instant_price` (
    `code` varchar(10) not null,
    `name` varchar(20) not null, 
    `timestamp` timestamp not null,
    `price` float not null,
    `percent` float not null
) engine = innodb default charset = utf8mb4;