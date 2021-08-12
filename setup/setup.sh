#!/bin/bash
RUN_USER=pi
RUN_GROUP=pi
PICAT_DIR=/usr/local/picat

cd "$(dirname "$0")"

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

function getNum {
	tmp=
	while true; do
		read -p "$1" tmp
		if [ -z $tmp ]; then
			tmp=$2
			return
		fi
		if ! { [[ $tmp ]] && [ $tmp -eq $tmp 2>/dev/null ]; }; then
			echo "Value was not a number! '$tmp'"
		else
			return
		fi
	done
}

echo "Press enter to skip and use defaults..."
read -p 'Person1 Name [Person1]: ' person1
read -p 'Person2 Name [Person2]: ' person2
getNum 'Hours between feeds [20]: ' 20
hoursBetweenFeeds=$tmp
getNum 'Screen inactivity sleep seconds [10]: ' 10
screenSleep=$tmp

echo ""
echo " -- GPIO Pins: Set to -1 if not used"
echo " -- Use GPIO pin number, NOT physical pin number"
getNum 'LED Pin: ' -1
ledPin=$tmp
getNum 'PIR Sensor output: ' -1
pirPin=$tmp

if [ -z "$person1" ]; then
	person1='Person1'
fi
if [ -z "$person2" ]; then
	person2='Person2'
fi
echo ""
echo "-- Using the following settings..."
echo "Person1 = $person1"
echo "Person2 = $person2"
echo "Hours Between Feeds = $hoursBetweenFeeds"
echo "Screen sleep seconds = $screenSleep"
echo "LED Pin = $ledPin"
echo "PIR Pin = $pirPin"
read -p "Press any key to continue..."
if [ ! -e /usr/local/picat ]; then
	mkdir $PICAT_DIR
	mkdir "$PICAT_DIR/log"
	mkdir "$PICAT_DIR/scripts"
	mkdir "$PICAT_DIR/data"
fi
cp -Rf ../code/* $PICAT_DIR/scripts
chmod +x $PICAT_DIR/scripts/picat.py
chown -R $RUN_USER:$RUN_GROUP $PICAT_DIR
cp picat.service /etc/systemd/system/picat.service
sed -i "s/User=pi/User=$RUN_USER/g" /etc/systemd/system/picat.service
systemctl enable picat.service

CONFIG_FILE=$PICAT_DIR/scripts/picat.conf
sed -i "s/NAME1 = Person1/NAME1 = $person1/g" $CONFIG_FILE
sed -i "s/NAME2 = Person2/NAME2 = $person2/g" $CONFIG_FILE
sed -i "s/SCREEN_SLEEP_SEC = 10/SCREEN_SLEEP_SEC = $screenSleep/g" $CONFIG_FILE
sed -i "s/HOURS_BETWEEN_FEEDS = 20/HOURS_BETWEEN_FEEDS = $hoursBetweenFeeds/g" $CONFIG_FILE
sed -i "s/LED_PIN = -1/LED_PIN = $ledPin/g" $CONFIG_FILE
sed -i "s/PIR_PIN = -1/PIR_PIN = $pirPin/g" $CONFIG_FILE

apt-get update
# Make sure python3 is installed
apt-get install -y python3-pip
# This handy script sets up all the dependencies.
echo "Running raspi-blinka.py... this might take a while."
python3 raspi-blinka.py

