#!/usr/bin/python

# telnet program example
import socket, select, string, sys, time, json

from message import Message

def Input():
    while True:
        print("""
        1. getSlides()
        2. heartbeat()
        3. getHardware()
        4. List Groups that a User is in
        5. List Users that are in 12 or more groups
        6. Suggest a cleanup
        7. Quit
        """)
        selection = raw_input("Select an option [1-7] \n")
        if selection == "1":
            jsonRequest = getSlides()
            break
        elif selection == "2":
            jsonRequest = heartbeat()
            break
        elif selection == "3":
            jsonRequest = getHardware()
            break
        elif selection == "4":
            userInGroup(Users)
        elif selection == "5":
            moreThan12(Users)
        elif selection == "6":
            suggest(Groups, Users)
        elif selection == "7":
            loop = False
        else:
            print "nope"
    return jsonRequest

def getSlides():
    jsonRequest = {}
    return jsonRequest

def heartbeat():
    jsonaAnswer = {}
    return jsonRequest

def getHardware():
    jsonRequest = {}
    return jsonRequest

def connect(host, port): 
    while True:
        # connect to remote host
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try :
            s.connect((host, port))
            print "Connected"
            break
        except :
            print 'Unable to connect'
            time.sleep(2)
    # Passes along PIE name to Grandma
    identify = Message("blueberry", "Grandma", "connect",{})
    identify.add_content("name","blueberry")
    identify.add_content("item2","bob")
    s.send(identify.toJSON())
    return s  

#main function
def main():
    host = "127.0.0.1"
    port = 5000
    
    s = connect(host, port)

    run = True
    
    while run:
        print 'Connected to remote host. Start sending messages'
	#Input()
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print "Disconnected"
                    s.close()
                    s = None
                    s = connect(host, port)
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = Input()
                s.send(msg.toJSON())

if __name__ == "__main__":
    main()
