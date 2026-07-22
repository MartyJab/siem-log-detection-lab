# Setup

## Installing docker
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker

## Build containers first time:
docker compose build --no-cache
docker compose up -d

## Start containers after first time:
docker compose up -d

## Excecute bash container
docker exec -it webserver bash
docker exec -it client bash
docker exec -it client2 bash

## Test
Client and Client2 bash:
curl http:webserver

Webserver: 
cat var/log/apache2/access.log 

## Install equirements client and client2
apt install -y python3-pip
source scripts/venv/bin/activate
python3 -m pip install -r scripts/requirements.txt


# Usage

## Run normal traffic on client or client2
python3 scripts/normal_traffic_simulation.py 

## Run suspicious traffic on client or client2
python3 scripts/path_scanner.py

## Run log reportin on webserver
python3 scripts/log_reporting.py

## Run log reportin on webserver
python3 scripts/log_detection.py


# Exit

## Exit terminal in client, client2 or webserver
exit

## Shut down docker containers in host terminal
docker compose down