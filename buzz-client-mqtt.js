const WebSocket = require('ws');
const mqtt = require('mqtt');
const { v4: uuidv4 } = require('uuid');
const buzztopic = `/neoosensory/sdk/python/${uuidv4()}/rumble`

function connect() {

  const ws = new WebSocket('ws://localhost:3141');
  const mqttClient = mqtt.connect('mqtt://broker.hivemq.com');


  function rumble(){
    let intencities = [];
    for (var i = 0; i < 40; i++) {
      intencities.push(Math.floor(Math.random() * 256))
    }
    intencities = intencities.concat([0, 0, 0, 0])
    ws.send(JSON.stringify(intencities));
  }

  ws.on('open', function open() {
    
    console.log("connected to web socket server");

    ws.send('device-info');
    ws.send('battery-info');

    //setInterval(rumble, 5000);
  });

  ws.on('message', function incoming(data) {
    console.log(data.toString());
  });

  ws.on('close', function incoming(data) {
    console.log("Server terminated");
    setTimeout(connect, 1000);
  });

  ws.on('error', () => {
    console.log("$$$ closed. Re-try...");
    setTimeout(connect, 1000);

  })

  mqttClient.on('connect', () => {
    console.log("Connected to MQTT ...");
    mqttClient.subscribe(buzztopic);
    
    console.log(`\nSubscribed to topic ${buzztopic}`);
    console.log(`Publish [255,255,255,255,0,0,0,0] to vibrate neosensory buzz.\n`);
  });

  mqttClient.on('disconnect', () => {
    console.log("Disonnected from MQTT ...");

  });
  mqttClient.on('message', (topic, message) => {

    try {
      if (topic === buzztopic) {
        console.log(message.toString());
        ws.send(message.toString());
      }

    } catch (error) {

    }
  });

}

connect();