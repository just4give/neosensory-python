### Interface Neosensory Buzz using python 

This reposority gives you sample code to connect to Neosensory buzz using Python library. As bluetooth requires OS mainlooop to process asynchronous BLE events, I have used python web socket to communicate with BLE events from outside of main loop. Web socket runs on port 3141. To communicate, all you need to do is write a web socket client listening on port 3141 and send message to buzz through web socket.

I have written `buzz-client-mqtt.js` client and you can send vibration frames via MQTT ( broker.hivemq.com ) 

#### This repo was tested on

- Mac 10.15.6 Catalina
- Raspberry Pi 4 32 bit 

```
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```


#### Setup Softwares on Raspberry Pi
Assuming you have Debian Buster installed. 

sudo apt-get update && \
sudo apt-get install -yq \
    build-essential \
    git wget  \
    bluetooth libbluetooth-dev libudev-dev libusb-1.0-0-dev \
    libusb-dev libdbus-1-dev libglib2.0-dev libical-dev libreadline-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-gi \
    python3-dbus \
    python3-setuptools \
  && sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*

  curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
  sudo apt-get install -y nodejs
  
  
  
  git clone https://github.com/donatieng/Adafruit_Python_BluefruitLE.git
  cd Adafruit_Python_BluefruitLE && sudo python3 setup.py install
  
  #### Clone and Run (same on both Mac and Pi)
  
  ```
  git clone https://github.com/just4give/neosensory-python.git
  cd neosensory-python
  pip3 install SimpleWebSocketServer
  python3 ble-central.py
  ```
  
  
  
  
  
  
