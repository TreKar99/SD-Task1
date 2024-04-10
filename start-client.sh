#!/bin/bash

# Function to display the menu
function display_menu() {
  echo "Chat Menu:"
  echo -e "\033[31m1. Connect to chat (private or group)\033[0m"
  echo -e "\033[32m2. Subscribe to group chat (create if non-existent)\033[0m"
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
      # Implement logic for connecting to a chat (private or group)
      echo "Option 1: Connect to chat"
      # Replace this with your actual implementation for connecting to a chat
      # It should prompt for chat ID and handle private/group chat scenarios
      # You might need to use tools like 'curl' or 'wget' to communicate
      # with the chat server
      ;;
    2)
      # Implement logic for subscribing to a group chat
      echo "Option 2: Subscribe to group chat"
      # Replace this with your actual implementation for subscribing to a group chat
      # It should prompt for chat ID and handle creating the chat if non-existent
      # You might need to use tools like 'curl' or 'wget' to communicate
      # with the chat server
      ;;
    3)
      echo "Option 3: Discover chats"
      python3 Redis/redisNameServer.py
      ;;
    4)
      echo "Option 4: Access insult channel"
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
