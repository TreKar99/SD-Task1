#!/bin/bash

# Comprobamos que se esté ejecutando en modo root
if [ $EUID -ne 0 ]; then
	echo " El script debe ejecutarse en modo root." >&2
	exit 1
fi

apt update 2</dev/null </dev/null

apt install rabbitmq-server redis -y 2</dev/null </dev/null

pip3 install pika
pip3 install redis
pip3 install -r private_chats/requirements.txt

echo "STARTING: rabbitmq-server"
sudo /usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management 2</dev/null </dev/null
systemctl is-active rabbitmq-server && systemctl restart rabbitmq-server 2</dev/null </dev/null || systemctl start rabbitmq-server 2</dev/null </dev/null 

echo "STARTING: redis-server"
redis-server 2</dev/null </dev/null &

echo "STARTING: gRPC"
python3 private_chats/gRPC_server.py

systemctl stop rabbitmq-server
systemctl stop redis-server
