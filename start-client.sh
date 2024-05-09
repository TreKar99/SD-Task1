#!/bin/bash

# Function to display the menu
function display_menu() {
  echo "Chat Menu:"
  echo -e "\033[31m1. Connect to private chat\033[0m"
  echo -e "\033[32m2. Connect to group chat\033[0m"
  echo -e "\033[33m3. Discover chats\033[0m"
  echo -e "\033[34m4. Access insult channel\033[0m"
  echo -e "\033[35m5. Exit\033[0m"
  echo -n "Enter your choice: "
  read choice
}

# Function to handle invalid input
function invalid_choice() {
  echo -e "\033[31mInvalid choice. Please enter a number between 1 and 5.\033[0m"
}

# Main loop for the menu
while true; do
#  clear
  display_menu

  case $choice in
    1)
      echo -e "\033[31mOption 1: Connect to private chat\033[0m"
      python3 private_chats/gRPC_client.py
      ;;
    2)
      echo -e "\033[32mOption 2: Connect to group chat\033[0m"
      echo "A quin grup chat et vols conectar?"
      read groupchat
      python3 RabbitMQPubSub/groupChat.py $groupchat
      ;;
    3)
      echo -e "\033[33mOption 3: Discover chats\033[0m"
      python3 Redis/redisNameServer.py
      #python3 ChatDiscovery.py
      ;;
    4)
      echo -e "\033[34mOption 4: Access insult channel\033[0m"
      python3 RabbitQueue/insultChannel.py
      ;;
    5)
      echo "Exiting..."
      exit 0
      ;;
    *)
      invalid_choice
      ;;
  esac

  # Wait for user to press Enter to continue
  read -p "Press Enter to continue..."
done
