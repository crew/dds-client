Server Functionality
=====================

Server will be a multi threaded program that will take inputs from the WP server as well as messages from the Clients. It will pass the appropriate data from the WP server to the appropriate Client as well as pass requests from the clients to the WP server

The "Socket Server" thread listens for messages from the client as well as send messages to the appropriate client when receiving a post from the WP server

The "WPHandler" thread listens for posts from the WP server and pass it to the socket server to send to the pies