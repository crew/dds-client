from message import Message
import json

# STUB COMMENT
##Params:##
# pie:
#     String
#     Returned Message object's src field.
#
# json_data:
#     String
#     JSON data. Check jsonToMessageContent
#     json_data specifications.
#
##Return:##
#
#     Message object
def message_creator(pie, json_data):
    return Message("Grandma", 
                   pie, 
                   "STATIC", 
                   json_extract(json_data));


# STUB COMMENT
##Params:##
# json_data:
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
def json_extract(json_data):
    result_dict = {};    
    json_dict = json.loads(json_data);
    for index, value in enumerate(json_dict["actions"]):
        result_dict[index] = value;
    return result_dict;
