import json

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

# variable to be increased to len(obj["actions"])
x = 0

# loops through all of the data in the json while using the duration to pause inbetween each entry
while x<len(obj["actions"]):
    print obj["actions"][x]["type"]
    print obj["actions"][x]["location"]
    time.sleep(obj["actions"][x]["duration"])
    if x<(len(obj["actions"])-1):
        x+=1
    else:
        x=0

