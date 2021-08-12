import board
import busio
from PIL import Image,ImageDraw,ImageFont
import adafruit_ssd1306

class OLED(object):
	def __init__(self):
		self.i2c = busio.I2C(board.SCL,board.SDA)
		self.disp = adafruit_ssd1306.SSD1306_I2C(128,64,self.i2c)
		self.width = self.disp.width
		self.height = self.disp.height
		self.canvas = Image.new("1",(self.width,self.height))
		self.draw = ImageDraw.Draw(self.canvas)
		self.disp.fill(0)
	
	def clear(self):
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
		self.disp.image(self.canvas)
		self.disp.show()

	def drawScreen(self):
		self.disp.image(self.canvas)
		self.disp.show()
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

	def addText(self,x,y,text,font):
		self.draw.text((x,y),text,font=font,fill="white")

