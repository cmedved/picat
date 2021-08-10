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

NAME1 = 'Person1'
NAME2 = 'Person2'
SLEEP_INACTIVITY_SEC = 60
FEED_INTERVAL_SEC = 20*3600
DATA_FILE='~/foodData.txt'
DATA_FILE=os.path.expanduser(DATA_FILE)

foodControl = FoodControl(DATA_FILE)

led = LED(25)
motionSensor = MotionSensor(24)
oled = OLED()
buttonA = Button(5) #NAME1
buttonB = Button(6) #NAME2
buttonUp = Button(17)
buttonDown = Button(22)
buttonLeft = Button(27)
buttonRight = Button(23)
buttonC = Button(4)

ms = MainScreen(oled,NAME1,NAME2)
bigScreen = BigScreen(oled,NAME1,NAME2)
curScreen = bigScreen
food = foodControl.getLastFiveFeeds()
data = {DataTypes.SHOULD_FEED: True, DataTypes.FOOD_LIST: food}
ms.updateItems(data)

screenOn = True
shouldSwitchScreen = False
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
led.on()
while True:
	if time.time() - lastActivity < SLEEP_INACTIVITY_SEC:
		screenOn = True
		food = foodControl.getLastFiveFeeds()
		shouldFeed = foodControl.shouldFeed(FEED_INTERVAL_SEC)
		data = {DataTypes.FOOD_LIST: food, DataTypes.SHOULD_FEED: shouldFeed}
		curScreen.updateItems(data)
		curScreen.drawScreen()
		oled.drawScreen()
		time.sleep(1)
	else:
		screenOn = False
		oled.clear()
		time.sleep(1)
	if shouldFeed:
		led.on()
	else:
		led.off()
	motion = motionSensor.motion_detected
	if motion:
		lastActivity = time.time()
	if shouldSwitchScreen:
		shouldSwitchScreen = False
		if curScreen == ms:
			curScreen = bigScreen
		else:
			curScreen = ms
