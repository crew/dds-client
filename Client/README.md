Client Functionality:
===================

Client will be a multithreaded program that will will take inputs from the server program as well as eventual hardware interactions. It will output to the display (A web browser), to the server, as well as possibly hardware.

The "main" thread essentialy is a thread manager that ensures all of the proper childern threads are running as well as pass along any information that they can't act upon.

The "display" thread manages "slide show" running on the browser front end as well as waits for any commands to upload the slides in the slide show, remove any slides from the slide show, immediatly display on the screen anything it may have to.

The "logging" thread waits input from any threads running and logs it to the syslog.

The "socket" thread handels the transfer of information between the server and the client. It will accomplish this through the use of sockets where PIEs will connect to a socket server running on the server and send a general identifier message. Then messages will pass freely between the server and client.