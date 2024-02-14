from pushbullet import pushbullet as pbclient
import os
import requests

#method 1
# connecting to the pushbullet api using my api key
pb = pbclient.Pushbullet("o.OvzdycciHIRvvwJKmEJXEwj5Si3gTEuJ")
#viewing all my devices list
print(f'Your devices are {pb.devices}')
#selecting my phone from devices
mydev = pb.get_device('Samsung SM-A736B')
#pushing a notification to my phone
push = mydev.push_note("Alert!!","boso ya gama3a project el networks elly sha8al gdn")
print('notification sent to user')

# method 2
#using curl to pass an http/https request directly into the command line
os.system('''curl --header 'Access-Token: <your_access_token_here>' \
     --header 'Content-Type: application/json' \
     --data-binary '{"body":"Space Elevator, Mars Hyperloop, Space Model S (Model Space?)","title":"Space Travel Ideas","type":"note"}' \
     --request POST \
     https://api.pushbullet.com/v2/pushes''')

#method 3
#using requests library 
