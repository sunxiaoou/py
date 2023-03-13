#! /bin/sh

createTable() {
mysql -u $user -p$pass $db << EOF
  DROP TABLE IF EXISTS $table;
  SET character_set_client = utf8mb4;
  CREATE TABLE $table (
    timestamp INT NOT NULL,
    C000010 FLOAT,
    C000015 FLOAT,
    C000016 FLOAT,
    C000300 FLOAT,
    C000688 FLOAT,
    C000827 FLOAT,
    C000852 FLOAT,
    C000903 FLOAT,
    C000905 FLOAT,
    C000906 FLOAT,
    C000919 FLOAT,
    C000922 FLOAT,
    C000925 FLOAT,
    C000932 FLOAT,
    C000978 FLOAT,
    C000989 FLOAT,
    C399001 FLOAT,
    C399006 FLOAT,
    C399324 FLOAT,
    C399330 FLOAT,
    C399393 FLOAT,
    C399550 FLOAT,
    C399701 FLOAT,
    C399702 FLOAT,
    C399812 FLOAT,
    C399967 FLOAT,
    C399975 FLOAT,
    C399986 FLOAT,
    C399989 FLOAT,
    C399995 FLOAT,
    C399997 FLOAT,
    C707717 FLOAT,
    C930653 FLOAT,
    C930697 FLOAT,
    C930743 FLOAT,
    C930782 FLOAT,
    C931009 FLOAT,
    C931068 FLOAT,
    C931142 FLOAT,
    C931187 FLOAT,
    C931357 FLOAT,
    C950090 FLOAT,
    CSPSADRP FLOAT,
    H30094 FLOAT,
    H30533 FLOAT,
    HSCAIT FLOAT,
    HSCEI FLOAT,
    HSI FLOAT,
    HSTECH FLOAT,
    IXY FLOAT,
    NDX FLOAT,
    S5INFT FLOAT,
    SPG120035 FLOAT,
    SPHCMSHP FLOAT,
    SPX FLOAT,
    sh000985 FLOAT NOT NULL,
    star FLOAT NOT NULL,
    PRIMARY KEY (timestamp)
  ) engine = innodb default charset = utf8mb4;
EOF
}

createTable2() {
mysql -u $user -p$pass $db << EOF
  DROP TABLE IF EXISTS $table;
  SET character_set_client = utf8mb4;
  CREATE TABLE $table (
    date TIMESTAMP NOT NULL,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(20) NOT NULL,
    open FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    close FLOAT NOT NULL,
    volume INT NOT NULL,
    PRIMARY KEY (date, code)
  ) engine = innodb default charset = utf8mb4;
EOF
}

createTable3() {
mysql -u $user -p$pass $db << EOF
  DROP TABLE IF EXISTS $table;
  SET character_set_client = utf8mb4;
  CREATE TABLE $table (
    date TIMESTAMP NOT NULL,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(20) NOT NULL,
    platform VARCHAR(10),
    currency VARCHAR(10) NOT NULL,
    type VARCHAR(10) NOT NULL,
    risk INT NOT NULL,
    nav FLOAT,
    market_value FLOAT NOT NULL,
    hold_gain FLOAT NOT NULL,
    PRIMARY KEY (date, code)
  ) engine = innodb default charset = utf8mb4;
EOF
}

createTable4() {
mysql -u $user -p$pass $db << EOF
  DROP TABLE IF EXISTS $table;
  SET character_set_client = utf8mb4;
  CREATE TABLE $table (
    date TIMESTAMP NOT NULL,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(20) NOT NULL,
    rank_170 INT,
    redeem_days VARCHAR(20),
    status VARCHAR(10) NOT NULL,
    PRIMARY KEY (date, code)
  ) engine = innodb default charset = utf8mb4;
EOF
}

insertTable() {
mysql -u $user -p$pass $db << EOF
  INSERT INTO $table (code, name, reference, lowest, low, high, highest, onsite, offsite)
    VALUES ('C000906', '中证800', '市盈率', 9, 15, 19, 52, '515800', '010763');
EOF
}

selectTable() {
mysql -u $user -p$pass $db << EOF
  # SELECT * FROM $table;
  SELECT * FROM $table ORDER BY timestamp DESC LIMIT 1;
  SELECT COUNT(*) FROM $table;
EOF
}


## main ##

if [ $# -lt 4 ]
then
  echo "$0 user pass db table"
  exit 1
fi

user=$1
pass=$2
db=$3
table=$4

createTable4
# insertTable
# selectTable

# echo $db.$table.sql
# mysqldump -u $user -p$pass -h localhost $db $table > /tmp/$db.$table.sql

# mysql -u $user -p$pass -h centos1 $db < /tmp/$db.$table.sql