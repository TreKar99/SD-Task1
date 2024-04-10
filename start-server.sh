#!/bin/bash

# Comprobamos que se esté ejecutando en modo root
if [ $EUID -ne 0 ]; then
	echo " El script debe ejecutarse en modo root." >&2
	exit 1
fi

apt update

apt install rabbitmq-server -y
apt install redis

pip3 install pika
pip3 install redis

echo "STARTING: rabbitmq-server"
systemctl is-active rabbitmq-server && systemctl restart rabbitmq-server || systemctl start rabbitmq-server

echo "START: redis-server"
redis-server 2</dev/null
