# Report device load stats to Watson IoT Platform
import os
import time
import json
import ibmiotf.device
from datetime import datetime

#The following file must be updated before running this program
configFilePath='./device.cfg'
waitInterval=[1]

def get_system_load():
	load = json.loads(os.popen('./sys-stats.sh').read())
	load['timestamp'] = datetime.now().isoformat()
	return load

try:
  options = ibmiotf.device.ParseConfigFile(configFilePath)
  client = ibmiotf.device.Client(options)
  client.commandCallback = command_callback
except ibmiotf.ConnectionException  as e:
	print "Error connecting to Watson IoT", e
	os.exit(1)

client.connect()

while True:
	data = get_system_load()
	client.publishEvent("status", "json", data)
	time.sleep(waitInterval[0])

