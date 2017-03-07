import random
import time
import os
import re
import tweepy

##
# Variables
##
# TWEEPY STUFF
# enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'pMoKjbV5ljdVlyzcsRtVcYOff'	# keep the quotes, replace this with your consumer key
CONSUMER_SECRET = '7tOh0Sq5gTQSQMHdEs8t7G7GXozqpHtrYFHqNM5qQbeSU0RZUX'	#k eep the quotes, replace this with your consumer secret key
ACCESS_KEY = '839020700471963648-7bsrQirguu24DZi9VEOu2bM7MS37mhX'	# keep the quotes, replace this with your access token
ACCESS_SECRET = 'eMwinILJVcHR9tyHAnY0SUlSIYx524YPeOCSR6te2c5UQ'	# keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

##
# Methods
##
def select_hp_line():
	books = []
	for root, dir, files in os.walk('.'):
		for file in files:
			if 'book' in file.lower():
				books.append(file)
	book = random.choice(books)

	lines = []
	
	with open(book, 'r') as f:
		lines = f.readlines()

	# select a semi random line that fits certain criteria
	valid_line = False
	line = ''
	while not valid_line:
		line = random.choice(lines)
		if len(line) > 140:	# line cannot be more than 140 (and cannot be 0)
			line = re.findall('.{%d}' % 140, line)
		elif len(line) == 0:
			continue;
		elif line == line.upper():	# a line in all caps is a chapter name (we don't want chapters)
			continue;
		valid_line = True
	return line


##
# Main script
##
while True:
	line = select_hp_line()

	try:
		print line  # local console check to see if line is valid
		api.update_status(status=line) 
		# api.update_with_media(filename,line) # tweets pictures
	except tweepy.error.TweepError:
		pass
	time.sleep(600)	# run every 10 minutes
