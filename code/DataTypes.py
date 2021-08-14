from enum import Enum
import time
from datetime import datetime, timezone

class FoodLog(object):
	def __init__(self,person,time):
		self.person = person
		self.time = int(time)

	def getFormattedTime(self):
		localTime = datetime.fromtimestamp(self.time)
		return localTime.strftime('%m/%d %H:%M')

	def getPerson(self):
		return self.person

class DataTypes(Enum):
	# Different types of data we can pass around
	FOOD_ENTRY = 1
	FOOD_LIST = 2
	SHOULD_FEED = 3
