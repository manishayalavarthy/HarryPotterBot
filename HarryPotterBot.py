import random
import time
import os
import re
import pickle

import tweepy
import markovify


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

# DESIRED QUOTE FORMAT FOR RE
# courtesy to https://gist.github.com/bpeterso2000/11277541
RE_QUOTES = re.compile(r"(?P<quote>[\"])(?P<string>.*?)(?<!\\)(?P=quote)")

# DATA
PICKLE_FILEPATH = 'quotes.pickle'
character_names = ['Ron', 'Weasley', 'Ronald', 'Harry', 'Potter', 'Hermoine', 'Granger']
characters_lines = 	{'Ron': [],
				'Harry': [],
				'Hermoine': [],
				'Hagrid': [],
				'Other': [],
				}
books = []			# list of books 
books_content = {}	# dict of books and their content represented as ('book_txt_name': book_content)

##
# Methods
##
def load_books():
	# find all files in directory that have 'book' in its name
	for root, dir, files in os.walk('.'):
		for file in files:
			if 'book' in file.lower():
				books.append(file)

def read_books(parse_quotes=False, create_char_dicts=False):
	"""
	This method reads books from the list of files in books and stores the content of each book into a dictionary
	books_content. 
	@param parse_quotes: 
	"""
	# store into a dictionary of books and content with book file name as key 
	# and all content of book (each line in book) as value
	for book in books:
		with open(book, 'r') as f:
			lines = f.readlines()
			books_content[book] = lines

	# this section of code parses the contents of each book for only quotes 
	for content in books_content.values():
		if parse_quotes:
			content = _parse_quotes(content)
		if create_char_dicts:
			_create_char_line_dicts(content)

def _parse_quotes(content):
	"""
	This private method looks through all the lines of a series (list) of lines from a book and removes
	any lines that are not quotes. 
	:param: content: content of a book 
	:return: content: quotes within the content of a book
	"""
	for line in content:
		if line == line.upper():
			content.remove(line)
			continue
		elif "\"" not in line:
			content.remove(line)
			continue
	return content
		
def _create_char_line_dicts(quotes_content):
	"""
	This method attempts to parse through a book (list of lines) and append to the global dictionary
	of quotes belonging to certain key characters.
	:param quotes_content: list of lines (represented as strings)
	"""
	for line in quotes_content:
		# find a way to parse for names outside of quotes to note that they said the quote\

		# TODO(leongj11@gmail.com) - use the re to parse through for quotes
		# if RE_QUOTES.search(line): # see RE_QUOTES
		quote_split = line.split('"')
		# http://stackoverflow.com/questions/2076343/extract-string-from-between-quotations
		quote_content = quote_split[1::2]
		non_quote_content = ' '.join(quote_split[::2])
		speakers = _extract_speaker_from_text(non_quote_content)
		for char in speakers:
			if char not in characters_lines.keys():
				characters_lines[char] = []		# initializing a new empty key,value in dict for previously unmentioned char
			for quote in quote_content:
				characters_lines[char].append(quote)

def _extract_speaker_from_text(text):
	"""
	This method takes in a section of text and returns the name(s) of persons (or at least most Proper nouns) in the text.
	:param text: input text to extract speaker from (text not surrounded by quotes)
	:return: list of str names
	"""
	# http://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk

	# print 'text 222222222222222222222'
	# print text
	# for sent in nltk.sent_tokenize(text):
	# 	print 'sent 66666666666666666'
	# 	print sent
	# 	for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
	# 		print 'chunk 3333333333333'
	# 		print chunk
	# 		if hasattr(chunk, 'node'):
	# 			print '0000000000000000'
	# 			print ' '.join(c[0] for c in chunk.leaves())
	# 			# return [c[0] for c in chunk.leaves()]


	# tokens = nltk.tokenize.word_tokenize(text)
	# pos = nltk.pos_tag(tokens)
	# sentt = nltk.ne_chunk(pos, binary = False)
	# person_list = []
	# person = []
	# name = ""
	# for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
	# 	for leaf in subtree.leaves():
	# 		person.append(leaf[0])
	# 	if len(person) > 1: #avoid grabbing lone surnames
	# 		for part in person:
	# 			name += part + ' '
	# 		if name[:-1] not in person_list:
	# 			person_list.append(name[:-1])
	# 		name = ''
	# 	person = []
	# return person_list
	proper_nouns = []
	words_list = text.split(' ')	# split sentence into a list of words
	for word in words_list:
		if word == word.title() and word in character_names:
			proper_nouns.append(word)
	if len(proper_nouns) <= 0:
		proper_nouns.append('Other')
	return proper_nouns

##
# Main script
##

# load all the data
if os.path.exists(PICKLE_FILEPATH):
	characters_lines = pickle.load(open(PICKLE_FILEPATH, 'rb'))
else:	
	load_books()
	read_books(parse_quotes=True, create_char_dicts=True)
	pickle.dump(characters_lines, open(PICKLE_FILEPATH, 'wb'))

def call_hp_character_quotes():
	selected_char = random.choice(characters_lines.keys())	# choose a random character

	# build the model
	quote_model = markovify.Text(' '.join(characters_lines.get(selected_char) + characters_lines.get('Other')))

	# create line
	line = '"' + quote_model.make_short_sentence(125) + '" - ' + selected_char
	print 'CURRENT CHAR = ' + selected_char
	return line

def print_hp_quotes():
	books = []
	for root, dir, files in os.walk('.'):
		for file in files:
			if 'book' in file.lower():
				books.append(file)
	book = random.choice(books)

	# Get raw text as string.
	with open(book) as f:
		text = f.read()

	# Build the mobel.
	text_model = markovify.Text(text)

	hpline = text_model.make_short_sentence(140)
	return hpline

# markovify and make tweepy API calls and post tweet
while True:


	try:
		# local console output
		randomNum = random.randint(1, 1000)
		if randomNum % 2 == 0:
			line = print_hp_quotes()
			api.update_status(status=line) 
		else:
			line = call_hp_character_quotes()
			api.update_status(status=line) 
		# print 'CURRENT CHAR = ' + selected_char
		# print line

		# tweet post
		# api.update_status(status=line) 
		# api.update_with_media(filename,line) # tweets pictures
	except tweepy.error.TweepError as e:
		print e
		pass
	time.sleep(5)	# run every 5 seconds
