#!/bin/bash

# echo $DB_USER
dockerize -wait tcp://$DB_USER:$DB_PORT -timeout 20s