from gpiozero import LED
from gpiozero import MotionSensor
from gpiozero import Button
from ui.oled import OLED
from ui.MainScreen import MainScreen
from ui.BigScreen import BigScreen
from FoodControl import *
from DataTypes import *
import logging
import time
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

shouldSwitchScreen = False
lastActivity = 0

def main():
	# sigh.. globals, I'm sorry. Too lazy to do it right for this.
	global shouldSwitchScreen
	global lastActivity
	fileLocation = os.path.join(os.path.dirname(os.path.realpath(__file__)),'picat.conf')

	cfg = readConf(fileLocation)

	# Start variables. Set these!
	NAME1 = cfg['NAME1']
	NAME2 = cfg['NAME2']
	SLEEP_INACTIVITY_SEC = int(cfg['SCREEN_SLEEP_SEC'])
	FEED_INTERVAL_SEC = int(cfg['HOURS_BETWEEN_FEEDS'])*3600
	DATA_FILE = '/usr/local/picat/data/foodLog.txt'
	LED_PIN = int(cfg['LED_PIN'])
	PIR_PIN = int(cfg['PIR_PIN'])
	LED_OUTPUT=False
	MOTION_INPUT=False
	if LED_PIN >= 0:
		LED_OUTPUT=True
	if PIR_PIN >= 0:
		MOTION_INPUT=True

	# These are GPIO pin numbers, NOT physical pin numbers.
	led = None
	if LED_OUTPUT:
		led = LED(LED_PIN)
	motionSensor = None
	if MOTION_INPUT:
		motionSensor = MotionSensor(PIR_PIN)
	oled = OLED()
	buttonA = Button(5) #NAME1
	buttonB = Button(6) #NAME2
	buttonUp = Button(17)
	buttonDown = Button(22)
	buttonLeft = Button(27)
	buttonRight = Button(23)
	buttonC = Button(4)
	
	foodControl = FoodControl(DATA_FILE)
	
	# Yeah, this is how we're gonna switch between screens. I'm sorry.
	ms = MainScreen(oled,NAME1,NAME2)
	bigScreen = BigScreen(oled,NAME1,NAME2)
	curScreen = bigScreen
	food = foodControl.getLastFiveFeeds()
	data = {DataTypes.SHOULD_FEED: True, DataTypes.FOOD_LIST: food}
	ms.updateItems(data)
	
	screenOn = True
	shouldSwitchScreen = False

	# Simple callback function for the joystick to switch screens.
	def switchFunc():
		global shouldSwitchScreen
		global lastActivity
		if screenOn:
			shouldSwitchScreen = True
		lastActivity = time.time()
	buttonUp.when_pressed = switchFunc
	buttonDown.when_pressed = switchFunc
	buttonLeft.when_pressed = switchFunc
	buttonRight.when_pressed = switchFunc
	
	def buttonAFunc(button):
		global lastActivity
		lastActivity = time.time()
		foodControl.addFeed(NAME1)
	
	def buttonBFunc():
		global lastActivity
		lastActivity = time.time()
		foodControl.addFeed(NAME2)
	buttonA.when_pressed = buttonAFunc
	buttonB.when_pressed = buttonBFunc
	
	lastActivity = time.time()
	while True:
		if time.time() - lastActivity < SLEEP_INACTIVITY_SEC:
			# If there was button or motion sensor activity... draw to the OLED!
			screenOn = True
			food = foodControl.getLastFiveFeeds()
			shouldFeed = foodControl.shouldFeed(FEED_INTERVAL_SEC)
			data = {DataTypes.FOOD_LIST: food, DataTypes.SHOULD_FEED: shouldFeed}
			curScreen.updateItems(data)
			curScreen.drawScreen()
			oled.drawScreen()
			time.sleep(1)
		else:
			if screenOn:
				# Only need to clear the screen once to sleep.
				# Hardware should be OLED, so all black = OFF
				screenOn = False
				oled.clear()
				time.sleep(1)
		if shouldFeed:
			if led is not None:
				led.on()
		else:
			if led is not None:
				led.off()
		if motionSensor is not None:
			# Could have used a callback, but nearly all PIR go high for
			# a min of 2 seconds.
			motion = motionSensor.motion_detected
			if motion:
				lastActivity = time.time()
		if shouldSwitchScreen:
			# yikes
			shouldSwitchScreen = False
			if curScreen == ms:
				curScreen = bigScreen
			else:
				curScreen = ms
	
def readConf(confFile):
	lines = None
	result = {}
	with open (confFile) as f:
		lines = f.read().splitlines()
	for line in lines:
		vals = line.split('=')
		key = vals[0].strip()
		value = vals[1].strip()
		result[key] = value
	return result

main()
