import sys
import tweepy
import json
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer


def readParameters(parameterKey):

	# Scan through file to find parameterKey
	parameterKeyCounter = 0
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parameters.txt'), "r") as ifile:
		for line in ifile:
			line = line.rstrip().split('\t')

			# If parameterKey is found
			if line[0] == parameterKey:

				# Increment parameterKeyCounter
				parameterKeyCounter += 1

				# Get the data type and read in the data
				dataType = line[1]
				if dataType == "string":
					parameterValue = line[2]

	# If only one parameterKey was found, then return
	if parameterKeyCounter == 1:
		return parameterValue
	else:
		sys.exit("ERROR:\t" + parameterKey +  " in parameters.txt must occur exactly once.")


# Implementation for our listener
class StdOutListener(tweepy.StreamListener):
	''' Handles data received from the stream. '''

	# The constructor
	def __init__(self, numTweets, sid):
		self.sadPeople = []
		self.numTweets = int(numTweets)
		self.sid = sid
 
	# When a tweet occurs
    	def on_data(self, data):

    		# Change to JSON
        	tweetDecoded = json.loads(data)

		# Get username and text of tweet
		username = tweetDecoded['user']['screen_name'].encode('ascii', 'ignore')
		originalTweetText = tweetDecoded['text'].encode('ascii', 'ignore')
		tweetText = originalTweetText.lower().split()
		tweetId = str(tweetDecoded['id'])
		
		# Check for the consecutive words "bad day"
		badDay = False
		for i in range(0,len(tweetText)-1):
    			if (tweetText[i] == 'bad') and (tweetText[i+1] == 'day'):
				badDay = True

		# If indicators that it is a bad day exist
		if badDay:
	
			# Make sure tweet is not a Re-Tweet
			if 'rt' not in tweetText:

				# Check that the tweet has negative sentiment
				sentimentScores = self.sid.polarity_scores(originalTweetText)
				if sentimentScores['compound'] < 0.0:

					# Create the CSV data
					tweetText = ' '.join(tweetText)
					sadPersonCSVData = username + ',' + tweetId + ',' + originalTweetText

					# Print tweet found
					print tweetText + '\n'

					# Add CSV data and return if necessary
					self.sadPeople.append(sadPersonCSVData)
					if len(self.sadPeople) == self.numTweets:
						return False
				
    	def on_error(self, status_code):
        	print('Got an error with status code: ' + str(status_code))
        	return True # To continue listening
 
    	def on_timeout(self):
        	print('Timeout...')
        	return True # To continue listening


def getSadPeople(numTweets):

	# Read in authentication credentials from parameters.txt
	consumerKey = readParameters('consumerKey')
	consumerSecret = readParameters('consumerSecret')
	accessToken = readParameters('accessToken')
	accessTokenSecret = readParameters('accessTokenSecret')

	# Connect to the Twitter API
	auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessToken, accessTokenSecret)

	# Create a listener and begin streaming tweets
	sid = SentimentIntensityAnalyzer()
	listener = StdOutListener(numTweets, sid)
	stream = tweepy.Stream(auth, listener)
	stream.filter(track=['bad day i'], languages=['en'])

	# Return values
	return listener.sadPeople


if __name__ == '__main__':

	# Create a list of sad people
	numTweets = 5
	sadPeopleList = getSadPeople(numTweets)








	
