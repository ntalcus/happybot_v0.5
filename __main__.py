from bot import TwitterBot
from threading import *
import time

botty = TwitterBot()

class fifteenThread(Thread):

    def __init__(self):
        Thread.__init__(self)


    def run(self):
        while True:
            botty.wholesome_tweet()
            botty.send_message_to_new_users()
            time.sleep(15*60)

class everyDayThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            botty.follower_message()
            time.sleep(24*60*60)

if __name__ == '__main__':
    fift = fifteenThread()
    everyDay = everyDayThread()
    fift.start()
    everyDay.start()



