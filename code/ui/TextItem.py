from PIL import ImageFont
import logging
import os

logger = logging.getLogger(__name__)

class TextItem(object):
	def __init__(self,text=None,font=None):
		self.x = 0
		self.y = 0
		self.text = ""
		if font is None:
			self.font = self.getFont(8)
		if text is not None:
			self.setText(text)

	def setText(self,text):
		self.text = text
		(self.width,self.height) = self.font.getsize(text)
	
	def setPos(self,x,y):
		self.x = x
		self.y = y

	def draw(self,oled):
		#logging.debug("Drawing text "+self.text)
		oled.addText(self.x,self.y,self.text,self.font)

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def getFont(self,fontSize):
		fileLocation = os.path.join(os.path.dirname(os.path.realpath(__file__)),'slkscr.ttf')
		font = ImageFont.truetype(fileLocation,fontSize)
		return font

	def setSize(self,fontSize):
		self.font = self.getFont(fontSize)
