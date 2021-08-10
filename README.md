# PiCat Project
So, this project is full of not-so-good python code, but the goal is to create a device that can
be stuck to a wall that shows when you last fed some cats.

## Usage
1. Pressing the joystick in any direction switches to a different view.
2. The #5 and #6 button will record a feeding from different people. This can be edited at the
top of the script file.

## Tunables
NAME1: Name of first person
NAME2: Name of second person
SLEEP\_INACTIVITY\_SEC: Amount of inactivity before turning screen off
FEED\_INTERVAL\_SEC: How many second to wait to switch to "feed" mode.
DATA\_FILE: '~/foodData.txt'
DATA\_FILE: os.path.expanduser(DATA\_FILE)

## Hardware Used For Project
Specific hardware was used for this project, and most of the code is dependent on it.

* [Rapberry Pi Zero WH](https://www.adafruit.com/product/3708)
* [Adafruit 128x64 OLED Bonnet](https://www.adafruit.com/product/3531)
* [PIR Motion Sensor](https://www.adafruit.com/product/4871) (optional)
* LED & resistor (optional)
* A case of your choosing. i.e. [Adafruit Pi Zero Case](https://www.adafruit.com/product/3252) or [C4 Labs Zebra Zero](https://www.c4labs.com/product/zebra-zero-case-raspberry-pi-zero-zero-w-color-and-upgrade-options/)
