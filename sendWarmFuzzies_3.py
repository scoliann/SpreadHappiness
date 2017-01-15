import findSadPeople as fsp
from selenium import webdriver
import os
import random
import time
import sys


def readParameters(parameterKey):

	# Scan through file to find parameterKey
	parameterKeyCounter = 0
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parameters.txt'), 'r') as ifile:
		for line in ifile:
			line = line.rstrip().split('\t')

			# If parameterKey is found
			if line[0] == parameterKey:

				# Increment parameterKeyCounter
				parameterKeyCounter += 1

				# Get the data type and read in the data
				dataType = line[1]
				if dataType == 'string':
					parameterValue = line[2]
				if dataType == 'int':
					parameterValue = int(line[2])

	# If only one parameterKey was found, then return
	if parameterKeyCounter == 1:
		return parameterValue
	else:
		sys.exit('ERROR:\t' + parameterKey +  ' in parameters.txt must occur exactly once.')


def sendWarmFuzzies(sadPeopleList):

	def login(username, password, driver):

		# Open Twitter log in page
		driver.get('https://twitter.com/login')

		# Enter username and password and log in
		usernameField = driver.find_element_by_class_name('js-username-field')
		usernameField.send_keys(username)
		passwordField = driver.find_element_by_class_name('js-password-field')
		passwordField.send_keys(password + '\n')

		# Return driver
		return driver

	def generateMessage():

		# Create message for tweet	
		sentenceMaker = [
		['Hey', 'Yo', 'Hiii', 'What\'s up', 'Hello'], 
		['', ',', '..', '...'], 
		['', 'so', 'well'], 
		['I'], 
		['saw', 'noticed', 'heard'],
		['', 'that'],
		['you'],
		['were', 'are'],
		['having', 'experiencing'],
		['a'],
		['bad', 'poor', 'sad', 'lousy', 'crummy', 'rough', 'crappy', 'off'],
		['day'],
		['', ',', '.', '..', '...'],
		['Here\'s', 'Here is', 'I present you'],
		['a'],
		['', 'cute', 'adorable'],
		['kitten!', 'kitten! :)']]
		message = ''
		for wordList in sentenceMaker:
			wordChoice = random.choice(wordList)
			message = message + ' ' + wordChoice

		# Add random mutation to message for originality
		# 	Mutation will always be extending the last letter of a word (eg. hello -> helloooo)
		mutatedMessage = message.split()
		numMutations = random.randint(0, 3)
		for i in range(numMutations):

			# Don't choose a word that is one letter long
			while True:
				index = random.randint(0, len(mutatedMessage) - 1)
				if len(mutatedMessage[index]) > 1:
					break
			mutatedWord = mutatedMessage[index]
			lastLetter = mutatedWord[-1]
			mutationSize = random.randint(0, 3)
			for j in range(mutationSize):
				mutatedWord = mutatedWord + lastLetter
			mutatedMessage[index] = mutatedWord
		mutatedMessage = ' '.join(mutatedMessage)

		# Return generated message
		return mutatedMessage

	'''
	=====Main Logic for the function sendWarmFuzzies is below=====
	'''

	# Read in variables from parameters.txt
	serverUrl = readParameters('serverUrl')
	username = readParameters('happyLogOnName')
	password = readParameters('happyPassword')
	waitTime = readParameters('waitTime')

	# Initialize webdriver
	#	Try linux chrome driver first, then try windows chrome driver
	driver = webdriver.Remote(serverUrl, webdriver.DesiredCapabilities.CHROME)
	driver.implicitly_wait(30)

	# Log in
	driver = login(username, password, driver)

	# For each person, tweet them a warm fuzzy
	for sadPerson in sadPeopleList:

		# Get the info for each person
		username = sadPerson.split(',')[0] 
		tweetId = sadPerson.split(',')[1]
		sadPersonUrl = 'https://twitter.com/statuses/' + tweetId

		# For each sad person, open to their tweet
		driver.get(sadPersonUrl)

		# Wait a moment to load specific tweet
		print str(waitTime) + ' sec - loading specific tweet'
		time.sleep(waitTime)

		# Follow sad person
		followButton = driver.find_element_by_class_name('user-actions-follow-button')
		followButton.click()

		# Click reply button
		replyButton = driver.find_element_by_class_name('js-actionReply')
		replyButton.click()

		# Generate a custom message
		mutatedMessage = generateMessage()

		# Add message to tweet
		tweetReply = driver.find_element_by_id('tweet-box-reply-to-' + tweetId)
		tweetReply.send_keys(mutatedMessage)

		# Wait a moment to add message
		print str(waitTime) + ' sec - adding message'
		time.sleep(waitTime)

		# Get random warm fuzzy image and append a '\0' to change its hash value
		pictureFolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kittenPictures')
		chosenImage = random.choice([f for f in os.listdir(pictureFolder) if os.path.isfile(os.path.join(pictureFolder, f))])
		completeImagePath = os.path.join(pictureFolder, chosenImage)
		file = open(completeImagePath, 'rb').read()
		with open(completeImagePath, 'wb') as newImage:
	  		newImage.write(file + '\0')

		# Add warm fuzzy image to tweet
		uploadPhoto = driver.find_elements_by_name('media_empty')[1]
		uploadPhoto.send_keys(completeImagePath)

		# Wait a moment to add photo
		print str(waitTime) + ' sec - adding photo'
		time.sleep(waitTime)

		# Press send button
		sendTweet = driver.find_elements_by_class_name('replying-text')[1]
		sendTweet.click()

		# Wait a moment to send
		print str(waitTime) + ' sec - sending tweet'
		time.sleep(waitTime)

	# Close webdriver
	driver.close()


def main():

	# Try to make some people happy
	numHappyVictims = 1

	# Get list of sad people
	sadPeopleList = fsp.getSadPeople(numHappyVictims)

	# Send sad people warm fuzzies
	sendWarmFuzzies(sadPeopleList)


if __name__ == '__main__':
	main()

	# Copy and past the following code where needed when debugging on AWS
	'''
	f = open(str(os.path.dirname(os.path.abspath(__file__))) + '/ANSWERS', 'a')
	f.write(str(filePath))
	f.close()
	import sys
	sys.exit()		# Wait a moment to attach
	print str(waitTime) + ' sec - attaching image'
	time.sleep(waitTime)
	'''









