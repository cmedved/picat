from ui.oled import OLED
from ui.TextItem import TextItem
import logging
from DataTypes import *

logger = logging.getLogger(__name__)
ITEM_NAME_TITLE = 'title'
ITEM_NAME_NEEDS_FOOD = 'needsFood'
ITEM_NAME_FOOTER = 'footer'
ITEM_NAME_TIME = 'time'

class BigScreen(object):
	def __init__(self,oled,name1,name2):
		# Sure hope you're using a 128x64 screen
		self.items = {}
		self.oled = oled
		# I don't know why some text gets clipped.
		title = TextItem("PiCat")
		title.setPos(100,0)
		title.setSize(7)
		self.items[ITEM_NAME_TITLE] = title
		footer = TextItem("#5 "+name1+"    #6 "+name2)
		footer.setPos(0,56)
		footer.setSize(7)
		self.items[ITEM_NAME_FOOTER] = footer
		needsFood = TextItem("")
		needsFood.setSize(14)
		needsFood.setPos(0,10)
		self.items[ITEM_NAME_NEEDS_FOOD] = needsFood
		timeTxt = TextItem("")
		timeTxt.setSize(8)
		timeTxt.setPos(0,30)
		self.items[ITEM_NAME_TIME] = timeTxt
	
	def drawScreen(self):
		for itemName in (self.items):
			self.items[itemName].draw(self.oled)

	def updateItems(self,data):
		for key in data:
			if key == DataTypes.SHOULD_FEED:
				shouldFeed = data[key]
				if shouldFeed:
					self.items[ITEM_NAME_NEEDS_FOOD].setText('FEED KITTENS   ')
				else:
					self.items[ITEM_NAME_NEEDS_FOOD].setText('DO NOT FEED   ')
			if key == DataTypes.FOOD_LIST:
				lastFood = data[key]
				if len(lastFood) == 0:
					continue
				lastFood = lastFood[0]
				timeInHours = int((time.time() - lastFood.time)/3600)
				self.items[ITEM_NAME_TIME].setText("Last fed "+str(timeInHours)+" hours ago")


