#!/bin/bash
set -e  

docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
docker logs django_web_vehicle_ins -f