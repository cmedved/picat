# PiCat Project
So, this project is full of not-so-good python code, but the goal is to create a device that can be stuck to a wall that shows when you last fed some cats.

![Screenshot](resources/picat.png)

## Usage
1. Pressing the joystick in any direction switches to a different view.
2. The #5 and #6 button will record a feeding from different people. This can be edited at the top of the script file. Will only record once every 30 seconds.
3. Holding both button 5 and 6 for at least 3 seconds will delete the last record every 3 seconds. Pushing the buttons will still initially record a feed though, if not during the 30 second safety window.

There are only two views:
1. Screen that shows whether cats need food and the last feed time.
2. Screen that shows whether cats need food and the last 3 feeds.

## Tunables
The following can be set either during the setup script or /usr/local/picat/scripts/picat.conf
* NAME1: Name of first person
* NAME2: Name of second person
* SCREEN\_SLEEP\_SEC: Amount of inactivity before turning screen off
* HOURS\_BETWEEN\_FEEDS: How many second to wait to switch to "feed" mode.
* LED_PIN: Which GPIO pin to use for the LED output
* PIR_PIN: Which pin to use for a PIR motion sensor

## Hardware Used For Project
Specific hardware was used for this project, and most of the code is dependent on it.

* [Rapberry Pi Zero WH](https://www.adafruit.com/product/3708)
* [Adafruit 128x64 OLED Bonnet](https://www.adafruit.com/product/3531)
* [PIR Motion Sensor](https://www.adafruit.com/product/4871) (optional)
* LED & resistor (optional)
* A case of your choosing. i.e. [Adafruit Pi Zero Case](https://www.adafruit.com/product/3252) or [C4 Labs Zebra Zero](https://www.c4labs.com/product/zebra-zero-case-raspberry-pi-zero-zero-w-color-and-upgrade-options/)

## Setup
There is a setup directory with setup.sh that will handle all of the setup.

For the Pi itself, I would recommend Pi Lite OS with a [headless setup](https://www.raspberrypi.org/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi)

Don't forget to set your hostname and password!
* sudo vi /etc/hostname
* passwd

You may also want to edit the system timezone to your local time with sudo raspi-config.

## OLED Bonnet
Note: The OLED bonnet uses the following GPIO pins (not physical pin numbers)
* GPIO 5 = ButtonA
* GPIO 6 = ButtonB
* GPIO 17 = Joystick Up
* GPIO 22 = Joystick Down
* GPIO 27 = Joystick Left
* GPIO 23 = Joystick Right
* GPIO 4 = Joystick center

Personally, I messed up and soldered my LED AND motion sensor to already used pins because I thought the above were physical pin numbers. So for mine, I need to manually disable joystick up/down in the code :(

To add the PIR sensor and LED, I cut out a chunk of a proto board with a dremel tool (do it outside). I then place some LED legs I cut off in the desired holes and soldered them, letting extra solder go in. I had it attached to the raspberry pi for the soldering so the legs didn't go to deep into the holes and prevent attaching the bonnet to the pi. I dripped solder on the screen and killed a few pixels.. you may want to cover it.

I'd recommend the LED, the PIR is a lot of trouble if you want to do it nicely though. The LED only needs a GPIO and ground pin. I would recommend a 3-3.3V LED with a 4.7k ohm resistor (or none if you want it super bright). If using PIR as well, you will need 3.3V and another GPIO (or maybe you _could_ use two gpio).

## Credits
* raspi-blinka.sh from Adafruit.
* [Silkscreen Font](https://github.com/topfunky/sparklines/tree/master/fonts/silkscreen)
