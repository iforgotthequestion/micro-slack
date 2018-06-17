from slackclient import SlackClient


class SlackMessage:
    """ Send and request slack messages"""

    def __init__(self):
        print('__init__ contents')

    def helloWorld(self):
        print("hello world")

    def sendInstant(self, channel, message):
        sc.api_call("chat.postMessage", as_user="true", channel=channel, text=message)

    def sendInstantTo(self, name, message):
        userId = fetchUserNames()[name]

        # if no channel exists, open new channel. Store channel info
        imOpenResult = sc.api_call("im.open", user=userId)
        channel = imOpenResult['channel']['id']

        # send message to channel
        sendInstant(channel, message)




sm = SlackMessage()
sm.helloworld()
