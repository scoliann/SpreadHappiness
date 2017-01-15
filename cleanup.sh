#!/bin/bash
echo 'cleanup.sh running...'
pkill python
pkill java
pkill Xvfb
pkill chromedriver
pkill chrome
