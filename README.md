# SD-Task1
Work on different communication patterns present in distributed systems, implementing an online chat application on python with a client and a server. Different clients may share a server to connect the application. 

This work describes the implementation of a chat application in Python. The app allows private chats between two users and group chats with multiple participants. For communication, different technologies are used, the first of which is the Client, whose interface is executed by the user and which offers options to connect to existing chats (private or group), subscribe to new groups, discover active chats and enter an insult channel. The Server runs in a separate process and consists of two components a Name Server which uses Redis (or RabbitMQ) to store the relationship between user/group names and connection information and the Message Broker - uses RabbitMQ for group chats, discovery of chats and messages from the insult channel. Regarding Private Chats, the connection and exchange of messages between two users is done using gRPC. While Group Chats use RabbitMQ Exchanges for collective communication. Customers can subscribe, connect and message groups. Regarding Chat Discovery, this is implemented with RabbitMQ to find active chats through shared events, rather than a shared repository. Finally, there is also an Insult Channel that uses a RabbitMQ queue (rather than an Exchange) to demonstrate the difference and send insults to random clients.

The steps to run it:
1. Run start-server.sh
2. Run start-client.sh as many times in different terminals as clients in the application you want to start.
3. For each client a menu will appear where you can choose between:
    - Connect to private chat
    - Connect to group chat
    - Discover chats
    - Access insult channel
    - Exit
