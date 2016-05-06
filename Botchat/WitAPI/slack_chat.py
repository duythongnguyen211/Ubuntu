from slacker import Slacker
import logging
logging.captureWarnings(True)

if __name__ == '__main__':
    slack = Slacker('xoxp-7223527622-34610515559-36494765460-c1afe08206')

    # Send a message to #general channel
    # slack.chat.post_message('slackbot', 'Hello fellow slackers!')

    # Get users list
    response = slack.users.list()
    users = response.body['members']
    slack.rtm.start()

    # Upload a file
    # slack.files.upload('hello.txt')
