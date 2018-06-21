from slackclient import SlackClient
from pprint import pprint
import argparse
from config import userToken

# CLI argument parser, data, and options
parser = argparse.ArgumentParser()
# parser.add_argument("action", help="Action to execute")
parser.add_argument("action", help = "message, fetch, disp, fav")
parser.add_argument("target", help = "MESSAGE: group, user, \n DISPLAY: channels, im, groups, unreads, recent \n FAVORITES: display, add, remove, [name of favorite]\n SETUP")

args = parser.parse_args()
message = args.target

# Token Management
token = userToken
#other token types to be added

# Initialize slack API with token from config.py
sc = SlackClient(token)

# Fetch - User Names
def getUserNames():
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

# Fetch - Channels

def getChannels():
    channels = sc.api_call("channels.list")
    channels = channels["channels"]

    results = {}

    for channel in channels:
        name = channel['name']
        id = channel['id']
        results[name] = id

    return results
def getChannelName(channelId):
    channelInfo = sc.api_call("channels.info", channel=channelId)
    channel = channelInfo['channel']
    name = channel['name']
    return name
def getChannelHistory(channel):
    history = sc.api_call("channels.history", channel=channel)
    return history

# Fetch - Groups

def getGroups():

    # *** add *** group list object structure

    groupsList = sc.api_call("groups.list")
    groups = groupsList["groups"]

    results = {}

    for group in groups:
        name = group['name'] #
        # if is direct message group
        if name[0:3] == 'mdpm':
            print('mpdm')
            continue

        id = group['id']
        results[name] = id

    return results
def getGroupDirects():
    groupsList = sc.api_call("groups.list")
    groups = groupsList["groups"]

    results = {}

    for group in groups:
        name = group['name'] #
        # if is direct message group
        if name[0:3] == 'mdpm':
            print('mpdm')
            id = group['id']
            results[name] = id

    return results

# Print - Channels
def printChannels():
    print ('\n')
    print('<(*.*<)   Channels (public)  (>*.*)>\n')

    channelsList = getChannels()
    for keys in channelsList:
        print(keys)
def printChannelHistory(channel):

    print("*~.~*~.~*~.~*~.~*~.~*")
    print("    " + getChannelName(channel))
    print("*~.~*~.~*~.~*~.~*~.~*")

    names = getUserNames()
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

# Print - Groups

def printGroups():
    print ('\n')
    print('<(*.*<)   Groups (private)   (>*.*)>\n')

    channelsList = getGroups()
    for keys in channelsList:
        if keys[0:4] != "mpdm":
            print(keys)

    print ('\n')
    print('<(*.*<)   Directs (private)  (>*.*)>\n')

    channelsList = getGroups()
    for keys in channelsList:
        if keys[0:4] == "mpdm":
            keys = keys[5:]
            print(keys)

    print ('\n')

# messages
def sendInstant(channel, message):
    # send message (as user) to target ()
    sc.api_call("chat.postMessage", as_user="true", channel=channel, text=message)
def sendInstantTo(name, message):
    userId = getUserNames()[name]

    # if no channel exists, open new channel. Store channel info
    imOpenResult = sc.api_call("im.open", user=userId)
    channel = imOpenResult['channel']['id']

    # send message to channel
    sendInstant(channel, message)

printChannels()
printGroups()

# pprint(getChannels())
# printChannelHistory("CAWMBKPQT")


# getChannels()

##### Body

# Is known user?
# try:
#     name = casualToName(args.user)
# except KeyError:
#     print("Y(*o*)Y   Undefined User   Y(*o*)Y")
#
# try:
#     sendInstantTo(name, args.message)
# except:
#     print("Message failed to send (fail: sendInstantTo)")
