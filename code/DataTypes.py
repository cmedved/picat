from enum import Enum
import time

class FoodLog(object):
	def __init__(self,person,time):
		self.person = person
		self.time = int(time)

	def getFormattedTime(self):
		return time.strftime('%m/%d %H:%M', time.gmtime(self.time))

	def getPerson(self):
		return self.person

class DataTypes(Enum):
	FOOD_ENTRY = 1
	FOOD_LIST = 2
	SHOULD_FEED = 3
