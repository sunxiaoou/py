#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <username> <password> <backup_directory> <remote_host>"
    exit 1
fi

# Source MySQL credentials
USER=$1
PASSWORD=$2
DATABASE="portfolio"
BACKUP_DIR=$3

REMOTE_HOST=$4

# List of tables to back up
TABLES=("asset" "cvtb_rank_daily" "cvtbone_daily" "etf_daily" "threshold" "valuation")

# Ensure the backup directory exists
mkdir -p $BACKUP_DIR

# Loop through each table and create a dump
for TABLE in "${TABLES[@]}"
do
    echo "Backing up $TABLE..."
    mysqldump -u $USER -p$PASSWORD $DATABASE $TABLE > $BACKUP_DIR/$TABLE.sql
    if [ $? -eq 0 ]; then
        echo "$TABLE backup completed successfully."

        # Load the backup into the remote database
        echo "Loading $TABLE into remote database..."
        mysql -u $USER -p$PASSWORD -h $REMOTE_HOST $DATABASE < $BACKUP_DIR/$TABLE.sql
        if [ $? -eq 0 ]; then
            echo "$TABLE loaded into remote database successfully."
        else
            echo "Error loading $TABLE into remote database."
        fi
    else
        echo "Error backing up $TABLE."
    fi
done

echo "All backups and loads completed."