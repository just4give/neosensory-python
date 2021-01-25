### Interface Neosensory Buzz using python 

This reposority gives you sample code to connect to Neosensory buzz using Python library. As bluetooth requires OS mainlooop to process asynchronous BLE events, I have used python web socket to communicate with BLE events from outside of main loop. Web socket runs on port 3141. To communicate, all you need to do is write a web socket client listening on port 3141 and send message to buzz through web socket.

I have written `buzz-client-mqtt.js` client and you can send vibration frames via MQTT ( broker.hivemq.com ) 

#### This repo was tested on

- Mac 10.15.6 Catalina
- Raspberry Pi 4 32 bit (Debian Buster 10)



#### Setup Softwares on Raspberry Pi
Assuming you have Debian Buster installed. 

```
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
  
  ```
  
  #### Clone and Run (same on both Mac and Pi)
  
  ```
  git clone https://github.com/just4give/neosensory-python.git
  cd neosensory-python
  pip3 install SimpleWebSocketServer
  python3 ble-central.py
  ```
  You should see an output like below. 
  <img width="846" alt="Screen Shot 2021-01-25 at 3 32 57 PM" src="https://user-images.githubusercontent.com/9275193/105762656-a9f71080-5f22-11eb-8246-3352a56ecc66.png">
  
  Now turn on your neosensory buzz and put it in pairing mode by holding down both "+" and "-" buttons for few seconds until leds stop blinking. And you should see Buzz is discovered, connected, authorized and ready to vibrate.
  
  
<img width="860" alt="Screen Shot 2021-01-25 at 3 47 22 PM" src="https://user-images.githubusercontent.com/9275193/105764173-a2386b80-5f24-11eb-8209-6c36a01d6b1c.png">

Now open another terminal and issue below commands
```
npm install
node buzz-client-mqtt.js
```
You should see below output. Copy the topic from terminal.

<img width="1136" alt="Screen Shot 2021-01-25 at 3 50 44 PM" src="https://user-images.githubusercontent.com/9275193/105764542-1a9f2c80-5f25-11eb-998e-54dbfaf66c70.png">

Open any MQTT client such as MQTT Fx, connect to broker.hivemq.com and publish `[255,255,255,255,0,0,0,0]` to the topic. 

<img width="907" alt="Screen Shot 2021-01-25 at 3 53 13 PM" src="https://user-images.githubusercontent.com/9275193/105764996-b92b8d80-5f25-11eb-9234-7eb1afeb5a75.png">

You should feel the vibration on your buzz and some information on terminal.

<img width="877" alt="Screen Shot 2021-01-25 at 3 55 09 PM" src="https://user-images.githubusercontent.com/9275193/105765030-c6e11300-5f25-11eb-8e15-101d117ad9e2.png">

#### Demo from Raspberry Pi 4 

![ezgif com-gif-maker](https://user-images.githubusercontent.com/9275193/105768169-fb56ce00-5f29-11eb-9dc9-8e6a7a4bf8ae.gif)


#### Exit program on Mac
If you have trouble terminating the python program, find the process id and kill it.

```
ps aux|grep "ble-central.py"
```

  
  
  
  
  
  
  
