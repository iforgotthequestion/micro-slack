from slackclient import SlackClient
from pprint import pprint
import argparse

# args
parser = argparse.ArgumentParser()
# parser.add_argument("action", help="Action to execute")
parser.add_argument("user", help = "User to target")
parser.add_argument("message", help = "Message to send")

args = parser.parse_args()
message = args.message

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

def shortNameToName(name):
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

# channels
def fetchChannelName(channelId):
    channelInfo = sc.api_call("channels.info", channel=channelId)
    channel = channelInfo['channel']
    name = channel['name']
    return name

# messages
def sendInstant(channel, message):
    sc.api_call("chat.postMessage", as_user="true", channel=channel, text=message)

def sendInstantTo(name, message):
    userId = fetchUserNames()[name]

    # if no channel exists, open new channel. Store channel info
    imOpenResult = sc.api_call("im.open", user=userId)
    channel = imOpenResult['channel']['id']

    # send message to channel
    sendInstant(channel, message)

def getChannels():
    channels = sc.api_call("channels.list")
    channels = channels["channels"]

    results = {}

    for channel in channels:
        name = channel['name']
        id = channel['id']
        results[name] = id

    return results

def getChannelHistory(channel):
    history = sc.api_call("channels.history", channel=channel)
    return history

def printChannelHistory(channel):

    print("*~.~*~.~*~.~*~.~*~.~*")
    print("    " + fetchChannelName(channel))
    print("*~.~*~.~*~.~*~.~*~.~*")

    names = fetchUserNames()
    history = getChannelHistory(channel)
    messages = history['messages']
    nameSize = 14

    for i in messages:
        user = i['user']
        text = i['text']
        userName = ''
        for key in names:
            if names[key] == user:
                userName = key
                break
        if len(userName) > nameSize:
            userName = userName[0:nameSize - 1]
        if len(userName) < nameSize:
            userName = userName + ((nameSize - len(userName)) * " ")
        print(userName + ":      " + text)

printChannelHistory("CAWMBKPQT")


# getChannels()

##### Body

# Is known user?
# try:
#     name = shortNameToName(args.user)
# except KeyError:
#     print("Y(*o*)Y   Undefined User   Y(*o*)Y")
#
# try:
#     sendInstantTo(name, args.message)
# except:
#     print("Message failed to send (fail: sendInstantTo)")
