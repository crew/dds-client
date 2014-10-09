from message import mMessage
import json

# STUB COMMENT
##Params:##
# pie:
#     String
#     Returned Message object's src field.
#
# jsonData:
#     String
#     JSON data. Check jsonToMessageContent
#     jsonData specifications.
#
##Return:##
#
#     Message object
def jsonToMessage(pie, jsonData):
    return Message("Grandma", 
                   pie, 
                   "STATIC", 
                   jsonToMessageContent(jsonData));


# STUB COMMENT
##Params:##
# jsonData:
#     String
#     JSON Data. Must be enclosed as a
#     dictionary with key "actions" mapped
#     to a list of dictionaries.
#
##Return:##
#
#     A dictionary as a list, integer values
#     from 0 to n-1 mapped to n list of
#     dictionaries stated in the input.
def jsonToMessageContent(jsonData):
    resultDict = {};    
    jsonDict = json.loads(jsonData);
    for index, value in enumerate(jsonDict["actions"]):
        resultDict[index] = value;
    return resultDict;
