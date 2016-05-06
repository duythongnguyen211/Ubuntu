
import fbchat
import logging
logging.captureWarnings(True)

fbEmail = 'utschatbot@gmail.com'
fbPass = 'aA123456$!'


def receivemsg(mid, author_id, author_name, message, metadata):
    client.markAsDelivered(author_id, mid)
    client.markAsRead(author_id)
    print("%s said: %s" % (author_name, message))
    c = client.send(author_id, "Seen")
    if c:
        print "Sent"

client = fbchat.Client(fbEmail, fbPass)

if __name__ == '__main__':
    # client.on_message = receivemsg
    client.listen()

