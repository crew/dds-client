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

# Takes current time and then uses to duration to find the time for the json input to end
# Stops when the current time reaches the target time, then moves onto the next thing in the json
for x in obj["actions"]:
    print x["type"] + ": " + x["location"]
    target_time = datetime.datetime.now() + datetime.timedelta(seconds = x["duration"])
    while(datetime.datetime.now() < target_time):
        pass


