import findSadPeople as fsp
from selenium import webdriver
import os
import random
import time


def readParameters(parameterKey):

	# Scan through file to find parameterKey
	parameterKeyCounter = 0
	with open('parameters.txt', 'r') as ifile:
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


def login(username, password):

	# Open Twitter log in page
	driver = webdriver.Chrome()
	driver.get('https://twitter.com/login')

	# Enter username and password and log in
	usernameField = driver.find_element_by_class_name('js-username-field')
	usernameField.send_keys(username)
	passwordField = driver.find_element_by_class_name('js-password-field')
	passwordField.send_keys(password + '\n')

	# Return driver
	return driver


def sendWarmFuzzies(sadPeopleList, driver, waitTime):

	# For each person, tweet them a warm fuzzy
	for sadPerson in sadPeopleList:

		# Get the info for each person
		username = sadPerson.split(',')[0] 
		tweetId = sadPerson.split(',')[1]
		sadPersonUrl = 'https://twitter.com/statuses/' + tweetId

		# For each sad person, open to their tweet
		driver.get(sadPersonUrl)

		# Follow sad person
		followButton = driver.find_element_by_class_name('user-actions-follow-button')
		followButton.click()

		# Click reply button
		tweetReply = driver.find_element_by_class_name('js-actionReply')
		tweetReply.click()

		# Create message for tweet	
		sentenceMaker = [
		['Hey', 'Yo', 'Hiii', 'What\'s up', 'Hello'], 
		[','], 
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
		['', '..', '...'],
		['Here\'s', 'Here is', 'I present you'],
		['a'],
		['', 'cute', 'adorable'],
		['kitten!', 'kitten! :)']]
		message = ''
		for wordList in sentenceMaker:
			wordChoice = random.choice(wordList)
			message = message + ' ' + wordChoice

		# Add message to tweet
		tweetReply.send_keys(message)

		# Wait a moment to add message
		print str(waitTime) + ' sec - adding message'
		time.sleep(waitTime)

		# Get random warm fuzzy image and append a '\0' to change its hash value
		chosenImage = random.choice([f for f in os.listdir('kittenPictures') if os.path.isfile(os.path.join('kittenPictures', f))])
		file = open('kittenPictures/' + chosenImage, 'rb').read()
		with open('kittenPictures/' + chosenImage, 'wb') as newImage:
	  		newImage.write(file + '\0') 

		# Add warm fuzzy image to tweet
		filePath = os.getcwd() + '\\' + 'kittenPictures' + '\\' + chosenImage
		uploadPhoto = driver.find_elements_by_name('media_empty')[1]
		uploadPhoto.send_keys(filePath)

		# Wait a moment to attach
		print str(waitTime) + ' sec - attaching image'
		time.sleep(waitTime)

		# Press send button
		sendTweet = driver.find_elements_by_class_name('tweeting-text')[1]
		sendTweet.click()

		# Wait a moment to send
		print str(waitTime) + ' sec - sending tweet'
		time.sleep(waitTime)


def makeSadPeopleHappy(numHappyVictims):

	# Read in variables from parameters.txt
	username = readParameters('happyLogOnName')
	password = readParameters('happyPassword')
	waitTime = readParameters('waitTime')

	# Get list of sad people
	sadPeopleList = fsp.getSadPeople(numHappyVictims)

	# Log in
	driver = login(username, password)

	# For each person, tweet them a warm fuzzy
	sendWarmFuzzies(sadPeopleList, driver, waitTime)


if __name__ == '__main__':

	# Run the whole process of finding sad people and sending them warm fuzzies
	makeSadPeopleHappy(10)





