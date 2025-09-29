#!/bin/bash

MYSQL_CONTAINER_LOCAL="vehicle_mysql_db"
DB_NAME_LOCAL="VehicleInsuranceDB"
DB_USER="admin"
DB_PASS="A_123456"
DUMP_FILE="database.sql"
HOST_PATH="/home/manhduwcs/code-project-v2/vehicle-insurance-management"

echo "Dump data... "
docker exec -i $MYSQL_CONTAINER_LOCAL mysql -u$DB_USER -p$DB_PASS $DB_NAME_LOCAL < $HOST_PATH/$DUMP_FILE