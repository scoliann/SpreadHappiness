#!/bin/bash
echo 'setup.sh running...'
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99
nohup java -jar /home/ubuntu/environmentSetupFiles/selenium-server-standalone-2.53.0.jar -port 8080 -maxSession 10 -Dwebdriver.chrome.driver=/home/ubuntu/environmentSetupFiles/chromedriver -Djava.security.egd=file:///dev/urandom switch &

