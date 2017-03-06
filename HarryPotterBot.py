import tweepy
import random
import time

##
# Variables
##
# TWEEPY STUFF
# TODO: @Manisha - change the account that the twitter bot is linked to so when we run the bot, it doesn't post on your account.
# enter the corresponding information from your Twitter application:
CONSUMER_KEY = '84ManyyJVzyDW5ytFdQIJDbT3'	# keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'oU8JQ04NmA7sUryDpBKEWFVcFqn8DM3faD9EqVDW4KY8uw829Q'	#k eep the quotes, replace this with your consumer secret key
ACCESS_KEY = '247966969-sFtBF0QsU7DiKlKNPlHxMjjK6tDwAx3RXb2rdlZu'	# keep the quotes, replace this with your access token
ACCESS_SECRET = '87v0FSBl6igW4AWCtVzdefvugcS9KzcKPvvv02ShJLpfH'	# keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# LOCAL VARIABLES
BOOK_TITLE = 'HarryPotterBook'

##
# Methods
##
def select_hp_line():
	book = BOOK_TITLE + str(random.randint(1, 5))
	lines = []
	print book
	with open(book, 'r') as f:
		lines = f.readlines()
	line = ''
	while len(line) > 140 or len(line) == 0:
		line = random.choice(lines)
	return line


##
# Main script
##
while True:
	line = select_hp_line()

	try:
		print line  # local console check to see if line is valid
		# api.update_status(status=line) 
		# api.update_with_media(filename,line) # tweets pictures
	except tweepy.error.TweepError:
		pass
	time.sleep(10)	# run every 10 seconds
