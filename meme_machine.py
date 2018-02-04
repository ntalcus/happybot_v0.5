import praw
import secrets
import random


class MemeMachine:


	def get_meme(self):
		try:
			return self.wholesome.next().url
		except StopIteration:
			self.wholesome = self.reddit.subreddit(self.memesubs[random.randint(0, 3)]).hot(limit=50)
			self.wholesome.next()
			meme = self.wholesome.next()
			return meme.url

	def __init__(self):
		self.memesubs = ["wholesomememes", "babyelephantgifs", "eyebleach", "wholesomememes"]
		self.reddit = praw.Reddit(client_id=secrets.client_id,
                     client_secret=secrets.client_secret,
                     password=secrets.password,
                     user_agent=secrets.user_agent,
                     username=secrets.username)
		self.wholesome = self.reddit.subreddit(self.memesubs[random.randint(0, 3)]).hot(limit=100)
		self.wholesome.next()



	
