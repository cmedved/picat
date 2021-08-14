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
		f = open(self.fileLocation,'a+')
		f.close()
		self.foodLogs = []
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
