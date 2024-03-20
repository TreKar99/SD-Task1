#!/bin/bash

apt update 

apt install rabbitmq-server -y
pip3 install pika

systemctl enable rabbitmq-server
systemctl start rabbitmq-server


