## Inspiration
I have a few friends who absolutely love cute things:  animal videos, babies, you name it.  I personally have always found these sources to be slightly amusing, but the degree to which some of my friends positively react to cute thing is... unbelievable.  So, one day I found myself wondering how to make the world a happier place, and I had a novel solution:  send warm fuzzies to the people who need it most.  I have done numerous projects scraping Twitter before, so identifying people who are feeling depressed would not be a problem!  Additionally, I have made Twitter bots before, so sending warm fuzzies to these people was totally doable!  I set off to write some code that could identify sad people and send them a nice message and a little something to cheer them up.

## Attempt #1
In my first attempt for this project, I had one Twitter account do the scraping for sad people and the tweeting warm fuzzies.  The twitter bot lasted for about 2 hours before my account was banned from Twitter.  Upon inquiry, I found that "cold calling" Twitter users was strictly forbidden.  During those two hours, however, I had received phenomenal feedback, and I knew that I would eventually have to return to this project.

## Attempt #2 (Final Attempt)
In my second attempt, I took a ton of precautions to make sure that I was not banned from Twitter a second time.  The measures that I took are detailed as follows:
- 1) I created two Twitter accounts.  One to do the scraping for sad people, and one to send out the warm fuzzies.
- 2) I knew that I could not tweet at people through the Twitter API, or I would get banned again.  So I wrote code to send tweets through my browser using Selenium.
- 3) I use a Markov Chain with mutations to generate custom messages for each tweet.
- 4) A null bit is appended to the end of each image that I tweet to guarantee that the hash value of the image is different each time.
- 5) I follow the user before I tweet at them.  I figured that tweeting at someone who my account follows will look less suspicious.

## All About AWS
I was able to get my python scripts running successfully on my local machine after a little time.  My goal, however, was to have this code run on AWS as a bot.  It does very little to create a bot that requires your laptop to be on and running 100% of the time for it to work.  I needed to move my bot to the cloud.  So, I created a free account and moved my files to AWS.  Getting my code to work on AWS, however proved to be quite a challenge.  Setting up an environment from scratch proved to be very difficult.  Some of the difficulties I encountered:
- 1) Need to install all python packages.
- 2) Some AWS distributions only let you use yum.
- 3) When debugging, it is very likely someone on Stackoverflow has solved the problem for Ubuntu.  It is very unlikely that someone has solved your problem for Amazon's custom Linux distribution.  This made debugging painful.
- 4) Getting Selenium to run headlessly was a huge pain.  I eventually used Selenium Server because this was such a difficulty.
- 5) I learned (the hard way) that crontab runs from a different directory than the one that your .cron file is in.  This meant that I often had to specify files with absolute paths in my .cron file.

## Code Functionality
Every half hour, crontab runs, executing my code by doing the following:
- 1) startup.sh, a bash script, runs.  This script sets up the environmental dependencies that my python scripts will need.  This includes starting Selenium Server, and Vxfb (a virtual display to allow Selenium Server to run).
- 2) Account #1 scrapes Twitter to find a sad person.  The scraping is done by streaming tweets that contain the words "bad", "day", and "i".  It is then checked that the words "bad" and "day" are consecutive (thus guaranteeing that the person is talking about a bad day).  The word "i" is required to increase the likelihood that the person is talking about themselves having a bad day.  After a tweet meeting these parameters is found, sentiment analysis is run on the tweet using Vader.  Sentiment analysis is necessary to make sure that tweets such as "not a bad day!  i won the lottery!" are not accepted.  If Vader determines that the tweet is negative in nature, then the tweet's ID is returned.  Account #2 then uses Selenium Server to log into twitter, reply to the tweet, add a custom message, attach a picture of a kitten, and send the tweet.
- 3) cleanup.sh, a bash script, runs.  This script terminates processes associated with the project.  Closing processes after running is necessary to insure that the VM does not get bogged down with "runaway" processes that are not being used anymore.  This could slow down the VM, use resources, and become quite expensive.

## The Results
The response of Twitter users to my "SpreadTheHappys" bot was excellent!  The rate of interaction with my tweets in replying, liking, and retweeting was exceptionally high.  Also, the tweet to follower ration for my bot was high, with the bot gaining a new subscriber for about every 10 tweets.  Most importantly, however, the individuals my bot reached out to seemed to really appreciate the gesture.  I am very proud of this.  The goal of this project was to increase the happiness of the world, and I can say with certainty that this goal was achieved.  It might sound juvenile or silly to be proud of sending cat photos to strangers, but consider the situation in a different light:  How many depressed individuals have you reached out to today?  How many sad people have thanked you recently for bringing some joy into their day?  With my bot, I have concrete numbers for these questions that affirm I have succeeded in reaching my goal... with the "SpreadTheHappys" bot, the world is indeed a happier place, and that is something that I am very proud of.  Some responses that I have gotten to the bot are as follows:
- 1) aw I love cute kitties :) thank u <3
- 2) Awe that fr was so sweet Thank You <3 :)
- 3) Orite. Thanks for the kitten ;-)
- 4) :D
- 5) Awww I hate cats but this made me happy thank u stranger (,:
- 6) Aww thankyou @SpreadTheHappys :'0 <3 :'0 <3 
- 7) @SpreadTheHappys this real life made me laugh hard asf
- 8) well damn aw
- 9) aww thank you so much :D <3
- 10) omg, thank you
- 11) wait this is amazing thank you so much
- 12) there is a god!! T_T <3
- 13) OMG U ARE THE SWEETEST LITTLE THING :) :) :) thank u this actually makes me feel a lot better <3 <3
- 14) OH MY GOSH I LOVE YOU
- 15) aw thank you! I appreciate this. (Whisper: i like dogs more...)

## Things I Learned
The most valuable thing that I learned from this project was my way around AWS.  I will be able to set up other Twitter bots (and Tinder, etc.) much faster in the future.  Also, now that I’ve struggled my way through learning to run Selenium Server on AWS, this will be a very powerful tool for the future!








