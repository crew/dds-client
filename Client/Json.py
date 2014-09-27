import json
import datetime

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
x = 0
while x < len(obj["actions"]):
        print obj["actions"][x]["type"] + ": " + obj["actions"][x]["location"]
        target_time = datetime.datetime.now() + datetime.timedelta(seconds = obj["actions"][x]["duration"])
        while(datetime.datetime.now() < target_time):
            pass
        if x < (len(obj["actions"]) - 1):
            x+=1
        else:            
            x=0


