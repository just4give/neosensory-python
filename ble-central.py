
import sys
import os
import signal
from threading import Thread 
from time import sleep
import traceback
import uuid
import Adafruit_BluefruitLE
import json
import base64

# Define service and characteristic UUIDs used by the peripheral.
SERVICE_UUID = uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
RX_CHAR_UUID = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
TX_CHAR_UUID = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

# see: 
from SimpleWebSocketServer import *

CONNECTION_CHECK_DELAY=1

tx = None
rx = None
wsService = None
ws = None
client = None
_buzzConnected = False
buzz = None
def log(msg):
    print(msg)

def request_device_info():
        global tx
        global rx
        if rx is not None:
            rx.write_value("device info\n".encode())
            sleep(1)

def request_battery_info():
        global tx
        global rx
        if rx is not None:
            rx.write_value("device battery_soc\n".encode())
            sleep(1)

def notificationCallback(data):
    global client
    print('Received: {0}'.format(data))
    if client is not None:
        client.sendMessage(data)

def process_motor_vibrate(data):
    global tx
    global rx
    global buzz
    global _buzzConnected
    try:
        frames = json.loads(data)
        if len(frames)%4 == 0:
            if rx is not None:
                if buzz.is_connected == False:
                    log("ERROR: Buzz got disconnected. Should re-connect automatically...")
                else:
                    encodedframe = base64.b64encode(bytes(frames))
                    command = "motors vibrate {0}\n".format(encodedframe.decode())
                    rx.write_value(command.encode())
                    sleep((len(frames)/4)* 0.016)
                        


    except expression as e:
        log("ERROR: processing frames {0}".format(e.message))


class BuzzWebSocket(WebSocket):

    def handleMessage(self):
        print(self.data)
        if "device-info" in self.data:
            request_device_info()
        elif "battery-info" in self.data:
            request_battery_info()
        else:
            process_motor_vibrate(self.data)
        
    def handleConnected(self):
        global client
        client = self
        
        

    def handleClose(self):
        global client
        client = None
        print(self.address, 'closed')

        

class BLEAgent:
    
    def __init__(self):
        
        global ws
        global wsService

        self.keepRunning = True
        wsService = BuzzWebSocket
        ws = SimpleWebSocketServer('', 3141, wsService)
        self.ble = Adafruit_BluefruitLE.get_provider()
        self.ble.initialize()

    
    def startWebSocketServer(self):
        self.wsWorkerThread = Thread(target=self._websocket_worker)
        self.wsWorkerThread.daemon = True
        self.wsWorkerThread.name = 'WebSocketMsgWorker'
        self.wsWorkerThread.start()

    def _websocket_worker(self):
        global ws
        try:
            log("Starting WebSocket server")
            ws.serveforever()
        except Exception as err:
            log( "ERROR: WebSocker server error: " + err.message + ", stacktrace: " + repr(traceback.format_exc()))
            
        self.keepRunning = False

    def scan_for_buzz(self):
        
        try:
            
            print('Searching for Neosensory Buzz...')
            self.adapter.start_scan()
            
            # Scan for the peripheral (will time out after 60 seconds
            # but you can specify an optional timeout_sec parameter to change it).
            
            device = self.ble.find_device(service_uuids=[SERVICE_UUID])
            if device is None:
                raise RuntimeError('Neosensory Buzz not found...')
            return device
            
        finally:
            # Make sure scanning is stopped before exiting.
            self.adapter.stop_scan()
       
    def startBLE(self):
        log("Starting BLE Agent")
        global tx
        global rx
        global buzz
        global _buzzConnected

        tx = None
        rx = None
        _buzzConnected = False
        
        self.ble.clear_cached_data()  
        self.adapter = self.ble.get_default_adapter()
        self.adapter.power_on()
        
        log('Using adapter: {0}'.format(self.adapter.name))
        self.ble.disconnect_devices([SERVICE_UUID])
        
        while _buzzConnected == False:
            try:
                buzz = self.scan_for_buzz()
                _buzzConnected = True
            except BaseException as e:
                #print("Restart the program (2)")
                sleep(1)

        log('Neosensory Buzz Found ')
        buzz.connect() 
        try:
            log('Connected and discovering characteristic...')
            buzz.discover([SERVICE_UUID], [TX_CHAR_UUID, RX_CHAR_UUID])

            self.service = buzz.find_service(SERVICE_UUID)
            rx = self.service.find_characteristic(RX_CHAR_UUID)
            tx = self.service.find_characteristic(TX_CHAR_UUID)
            tx.start_notify(notificationCallback)
            
            sleep(2)
            rx.write_value("auth as developer\n".encode())
            rx.write_value("accept\n".encode())
            rx.write_value("audio stop\n".encode())
            rx.write_value("motors start\n".encode())
            while buzz.is_connected:
                sleep(1)
            
            print("Buzz is disconnected. End of event loop. Go back to start")
            self.startBLE()
            
        except Exception as err:
            log( "ERROR: Start BLE " + err.message + ", stacktrace: " + repr(traceback.format_exc()))

            
    
    def poll(self):
        global tx
        global rx
        global buzz
        global _buzzConnected
        while True:
            if rx is not None:
                if buzz.is_connected == False:
                    log("ERROR: Buzz got disconnected. Try re-connecting...")
                    tx = None
                    rx = None
                    _buzzConnected = False
                    self.ble.run_mainloop_with(self.startBLE)
                else:
                    frames = [0,0,0,255,0,0,0,0]
                    encodedframe = base64.b64encode(bytes(frames))

                    command = "motors vibrate {0}\n".format(encodedframe.decode())
                    rx.write_value(command.encode())
                    sleep(len(frames)* 0.016)
                    #rx.write_value("motors vibrate AAAAAA==\n".encode())
                    #sleep(5)
            sleep(5)
            
    def start(self):
        try:
            self.startWebSocketServer()
            #Thread(target=self.poll,daemon=True).start()
            self.ble.run_mainloop_with(self.startBLE)
            print("Should not come here")
            # while True:
            #     sleep(CONNECTION_CHECK_DELAY) 
            #     print("connection check..")       
            #     if not self.isConnected():
            #         break

        except Exception as err:
            log( "ERROR: Main (General) " + err.message + ", stacktrace: " + repr(traceback.format_exc()))
        
 

    def stop(self):
        global buzz
        global _buzzConnected
        log( "BLE Agent exiting...")        
        buzz.disconnect()
        _buzzConnected = False


if __name__ == "__main__":
    agent = BLEAgent()
    agent.start()  # will block until error (e.g. connection loss)
    agent.stop()

