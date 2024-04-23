#!/bin/bash

set -e 

docker rmi cmp_backend -f 
docker rm cmp_backend -f

docker-compose -f docker-compose.yml up --remove-orphans -d --build