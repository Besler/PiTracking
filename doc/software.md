# PiTracking - Software
Below are some notes on setting up the software on the Raspberry Pi.
These instructions are loose and only intended to guide you.

## Update Machine
Do some [standard updates](https://www.raspberrypi.org/documentation/raspbian/updating.md).
```bash
sudo apt-get update
sudo apt-get dist-upgrade
```

## Installing OpenCV
I followed a [tutorial](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/)
for installing OpenCV. This took roughly two hours to complete including compiling, download, and executing commands.
You can find images with OpenCV already installed if you want to skip this step.

From here on out and in the code, it is assumed you name your virtualenv _cv_.

## Setup GPIO and Camera Libraries
If you want to use GPIOs, you typically install the package through `apt-get`.
```bash
sudo apt-get install python-rpi.gpio
```

However, we want to install the python support into our virtual enviornment. With the
virtual environment activated, use pip. This also installs the picamera library.
```bash
pip3 install RPi.GPIO
pip3 install "picamera[array]"
```

## Clone this repository
I would recommend installing into your home directory. Otherwise, you will need to change
the scripts in the repository to point to your data.
```bash
cd
git clone https://github.com/Besler/PiTracking.git
```

## Run at boot
Finally, we want the program to run at boot.
```bash
# Install the run script
mv pitracker.sh /etc/init.d
cd /etc/init.d
chmod 0755  pitracker.sh
sudo chkconfig --add pitracker.sh
sudo systemctl daemon-reload

# Test it out!
sudo service pitracker.sh start
```
If the program fails when you start the service, it will fail when you restart the machine.
I found it took ~15 seconds to start the red LED on the camera. That is how I knew the program was on.
