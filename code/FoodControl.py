import logging
import os
import time
from DataTypes import *
logger = logging.getLogger()


class FoodControl(object):
	def __init__(self,fileLocation=None):
		if fileLocation is None:
			fileLocation = os.path.join(os.path.dirname(os.path.realpath(__file__)),'foodData.txt')
		self.fileLocation = fileLocation

		# Create the file?
		f = open(self.fileLocation,'a+')
		f.close()
		self.foodLogs = []

		# Load the file contents to mem
		with open(self.fileLocation) as f:
			content = f.readlines()
		content = [x.strip() for x in content]
		for x in content:
			vals = x.split(',')
			if len(vals) != 2:
				continue
			log = FoodLog(vals[1],vals[0])
			self.foodLogs.append(log)

	def getLastFeedData(self):
		if len(self.foodLogs) > 0:
			return self.foodLogs[-1]
	
	def addFeed(self,person):
		curTime = time.time()
		# Put a 30 sec delay in to prevent accidental double presses!
		if len(self.foodLogs) == 0 or curTime - self.foodLogs[-1].time > 30:
			with open(self.fileLocation,'a+') as f:
				f.write(str(int(curTime))+","+person+"\n")
				f.close()
			self.foodLogs.append(FoodLog(person,curTime))

	def getFeedsPerPersonThirtyDays(self):
		results = []
		curTime = time.time()
		oldestTime = 30*24*60*60
		for x in self.foodLogs:
			if curTime - x.time < oldestTime:
				results.append(x)
		return results

	def getLastFiveFeeds(self):
		# Note, first record is oldest feed
		results = []
		i = len(self.foodLogs)-1
		while i>=0 and len(results) < 5:
			results.append(self.foodLogs[i])
			i = i - 1
		return results
	
	def shouldFeed(self,timeSec):
		if len(self.foodLogs) == 0:
			return True
		lastData = self.getLastFeedData()
		secondsSinceFed = time.time() - lastData.time
		if secondsSinceFed > timeSec:
			return True
		else:
			return False

	def removeLastFeed(self):
		if len(self.foodLogs) > 0:
			del self.foodLogs[-1]
			# Efficiently delete last line of file.
			# https://stackoverflow.com/questions/1877999/delete-final-line-in-file-with-python
			with open(self.fileLocation,'r+') as f:
				f.seek(0, os.SEEK_END)
				pos = f.tell() - 1
				while pos > 0 and f.read(1) != "\n":
					pos -= 1
					f.seek(pos,os.SEEK_SET)
				if pos > 0:
					f.seek(pos,os.SEEK_SET)
					f.truncate()
