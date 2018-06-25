from slackclient import SlackClient
from pprint import pprint # remove once built
from time import strftime, localtime
import argparse, os, sys

try:  # check for user token in config.py -- prompts for input if none found
    from config import userToken
except:
    print("\nNo user token found. Running: 'slack install token'\n")
    tokenTemp = input('Enter the token for the workspace you wish to join: ')
    tokenFile = open('config.py', 'w')
    tokenFile.writelines("userToken=" + '"' + tokenTemp + '"')
    tokenFile.close()
    print("\nToken installed. Try running your command again\n")
    sys.exit()

# CLI argument parser, data, and options
parser = argparse.ArgumentParser()
# parser.add_argument("action", help="Action to execute")
parser.add_argument("action", help = "message, list, favorites, setup")
parser.add_argument("target", help = "MESSAGE: group, user, LIST: all, channels, im, groups, recent FAVORITES: list, add, remove, [# of favorite] SETUP: install, token")

args = parser.parse_args()
action = args.action
target = args.target

sc = SlackClient(userToken) # Initialize slack API with token from config.py


def getUserNames():
    users = sc.api_call("users.list", token=userToken)
    members = users['members']
    userList = {}

    i = 0
    while i < len(members):
        userData = members[i]
        name = userData['name']
        id = userData['id']
        realName = userData['real_name']
        userList[name] = id

        i += 1

    return userList
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
def getDirects():
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

def printChannels():
    print ('\n')
    print('<(*.*<)   Channels (public)  (>*.*)>\n')

    channelsList = getChannels()
    i = 1
    for keys in channelsList:
        print(str(i) + " " + keys)
        i += 1
    print('\n')
def printGroups():
    print ('\n')
    print('<(*.*<)   Groups (private)   (>*.*)>\n')
    i = 1
    groupsList = getGroups()
    for keys in groupsList:
        if keys[0:4] != "mpdm":
            print(str(i) + " " + keys)
        i += 1

    print ('\n')
def printDirects():
    print('\n')
    print('<(*.*<)     Directs          (>*.*)>\n')

    channelsList = getGroups()
    i = 1
    for keys in channelsList:
        if keys[0:4] == "mpdm":
            keys = keys[5:]
            print(str(i) + ' ' + keys)
            i += 1


    print ('\n')
def printUsers():
    print ('\n')
    print('<(*.*<)      Users         (>*.*)>\n')
    i = 1
    userList = getUserNames()
    for keys in userList:
        print(str(i) + ' ' + keys)
        i += 1
    print('\n')
def printAll():
    printChannels()
    printGroups()
    printDirects()

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
        time = float(i['ts'])
        userName = ''
        for key in names:
            if names[key] == user:
                userName = key
                break
        # print(strftime("%m/%d|%H:%M", localtime(time)) + " " + userName + ": " + text)

        if len(userName) > nameSize:
            userName = userName[0:nameSize - 1]
            print(strftime("%m/%d|%H:%M", localtime(time)) + " " + userName + ": " + text)
        if len(userName) < nameSize:
            userName = userName + ((nameSize - len(userName)) * " ")
            print(strftime("%m/%d|%H:%M", localtime(time)) + " " + userName + ": " + text)

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

if action == "setup":

    if target == "install": # fresh install
        os.system('bash setup.sh')

    if target == "token":
        tokenTemp = input('Enter the token for the workspace you wish to join: ')
        tokenFile = open('config.py', 'w')
        tokenFile.writelines("userToken=" + '"' + tokenTemp + '"')
        tokenFile.close()

if action == "list" or action == "l":

    if target == "group" or target == "g":
        printGroups() # prints list of groups

    if target == "direct" or target == "d":
        printDirects() # prints list of direct messages

    if target == "users" or target == "user" or target == "u":
        printUsers() # prints list of users

    if target == "channel" or target == "c":
        printChannels() # prints list of channels

if action == "message" or action == "m":

    if target.isnumeric() == True:
        print ("message " + target)

    if target == "group" or target == "g":
        print ("message: group")

    if target == "user" or target == "u":
        print ("message: user")

    if target == "channel" or target == "c":
        print ("message: channel")

if action == "favorites" or "f":

    if target == "list" or target == "l":
        print ("favorites: list")

    if target == "add" or target == "a":
        print ("favorites: add")

    if target == "remove" or target == "r":
        print ("favorites: remove")

    if target.isnumeric() == True:
        print ("favorites " + target)


# printAll()
# printChannelHistory("CAWMBKPQT")
# pprint(getUserNames())

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
