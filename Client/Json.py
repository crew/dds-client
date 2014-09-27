import json
import Queue
import msvcrt
import datetime

data = {"type":"slide", "location":"www.reddit.com", "duration":2} 
q = Queue.Queue(0)
q.put(data)

# all of the information to be sent to be displayed
obj = {
    "actions":[
        {
            "type":"slide",
            "location":"http:\/\/m.weather.com\/weather\/tenday\/USMA0046",          
            "duration":10
        },
        {
            "type":"slide",
            "location":"http:\/\/www.northeastern.edu\/news\/",
            "duration":10
        },
        {
            "type":"slide",
            "location":"http:\/\/dds-wp.ccs.neu.edu\/?slide=cisters-welcome-dinner&pie_name=chocolate",
            "duration":10
        },
        {
            "type":"slide",
            "location":"http:\/\/dds-wp.ccs.neu.edu\/?slide=fall-masters-student-social&pie_name=chocolate",
            "duration":10
        },
        {
            "type":"slide",
            "location":"http:\/\/dds-wp.ccs.neu.edu\/?slide=test-ccis-tutoring&pie_name=chocolate",
            "duration":10
        },
        {
            "type":"slide",
            "location":"http:\/\/dds-wp.ccs.neu.edu\/?slide=cisters&pie_name=chocolate",
            "duration":10
        },
        {
            "type":"slide",
            "location":"http:\/\/dds-wp.ccs.neu.edu\/?slide=welcome-to-the-ccis-main-office&pie_name=chocolate",
            "duration":10
        }
    ]
}

#Loops through the Json and outputs the data
#Once it reaches the end of the data it resets
#If "a" key is pressed, then it adds the next slide in the queue to the JSON
#if "r" key is pressed, puts fram back into queue, then it removes the last slide in the JSON
#prints "at last frame!" if you press r to the last frame
x = 0
while x < len(obj["actions"]):
        print obj["actions"][x]["type"] + ": " + obj["actions"][x]["location"]
        target_time = datetime.datetime.now() + datetime.timedelta(seconds = obj["actions"][x]["duration"])
        while(datetime.datetime.now() < target_time):
            pass
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == 'a':
                    if not q.empty():
                        currentMessage = q.get()
                        obj["actions"].append(currentMessage)
                elif key == 'r':
                    if len(obj["actions"]) > 1:
                            q.put(obj["actions"][(len(obj["actions"]) - 1)])
                            del obj["actions"][(len(obj["actions"])-1)]
                    else:
                            print "at last frame!"
                else:
                    pass
        if x < (len(obj["actions"]) - 1):
            x+=1
        else:            
            x=0



