'''Read json file save it into list'''

import json

#read json file
def readJson(path):
    try:
        with open(path,'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError as err:
        print(err)
    except IOError:
        print("Error: Could not open the file.")
    return data