from slackclient import SlackClient
from pprint import pprint
import argparse

# args
parser = argparse.ArgumentParser()
# parser.add_argument("action", help="Action to execute")
parser.add_argument("user", help = "User targeted by action")
parser.add_argument("message", help = "Message to send")

args = parser.parse_args()

# user token
token = 'xoxp-322488135875-322034850833-381991675365-bc90aa8f4ef622b2fee8ad5220b82ddf'
sc = SlackClient(token)

# users

def fetchUserNames():
    users = sc.api_call("users.list", token=token)
    members = users['members']

    userList = {}

    i = 0
    while i < len(members):
        userData = members[i]
        name = userData['name']
        id = userData['id']
        userList[name] = id

        i += 1

    return userList

def convertName(name):
    userList = {
        'will': 'will.kasten',
        'anton': 'ajsurunis',
        'ivan': 'ivanmccarter',
        'jess': 'jstothers220',
        'jamil': 'jvalliswalker',
        'michaela': 'michaelamstewart17',
        'suz': 'suzmokie',
        'rees': 'riscblanchard',
        'bozek': 'sambozek'
    }

    return userList[name]

print(convertName(args.user))

def sendInstant(channel, message):
    sc.api_call("chat.postMessage", as_user="true", channel=channel, text=message)

def sendInstantTo(name, message):
    userId = fetchUserNames()[name]

    # if no channel exists, open new channel. Store channel info
    imOpenResult = sc.api_call("im.open", user=userId)
    channel = imOpenResult['channel']['id']

    # send message to channel
    sendInstant(channel, message)

try:
    sendInstantTo(convertName(args.user), args.message)
except NameError:
    print("nameError")



# pprint(fetchUserNames())
# sendInstantTo("will.kasten", "I sent this message from my command line!")
