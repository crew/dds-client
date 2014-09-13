#!/usr/bin/python

# telnet program example
import socket, select, string, sys, time, json

from message import Message

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

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
        prompt()

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
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()

if __name__ == "__main__":
    main()
