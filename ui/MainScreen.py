from ui.oled import OLED
from ui.TextItem import TextItem
import logging
from DataTypes import *

logger = logging.getLogger(__name__)
ITEM_NAME_TITLE = 'title'
ITEM_NAME_NEEDS_FOOD = 'needsFood'
ITEM_NAME_FEED_LIST = 'feedList'
ITEM_NAME_PERSON_LIST = 'personList'

class MainScreen(object):
	def __init__(self,oled,name1,name2):
		self.items = {}
		self.oled = oled
		title = TextItem("#5 "+name1+"    #6 "+name2)
		title.setPos(0,56)
		title.setSize(7)
		self.items[ITEM_NAME_TITLE] = title
		needsFood = TextItem("")
		needsFood.setSize(10)
		needsFood.setPos(0,0)
		self.items[ITEM_NAME_NEEDS_FOOD] = needsFood
		foodList = TextItem("")
		foodList.setPos(40,16)
		self.items[ITEM_NAME_FEED_LIST] = foodList
		personList = TextItem("")
		personList.setPos(0,20)
		self.items[ITEM_NAME_PERSON_LIST] = personList
		
	
	def drawScreen(self):
		for itemName in (self.items):
			self.items[itemName].draw(self.oled)

	def updateItems(self,data):
		for key in data:
			if key == DataTypes.FOOD_LIST:
				personText = ""
				foodText = ""
				foodList = data[key]
				i = 0
				while i < len(foodList) and i < 3:
					item = foodList[i]
					personText += item.person+"\n"
					foodText += item.getFormattedTime()+"\n"
					i = i + 1
				self.items[ITEM_NAME_FEED_LIST].setText(foodText)
				self.items[ITEM_NAME_PERSON_LIST].setText(personText)
			elif key == DataTypes.SHOULD_FEED:
				shouldFeed = data[key]
				if shouldFeed:
					self.items[ITEM_NAME_NEEDS_FOOD].setText('   FEED KITTENS   ')
				else:
					self.items[ITEM_NAME_NEEDS_FOOD].setText('   DO NOT FEED   ')


