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

	
def command_callback(cmd):
	print("Incomming command from Watson IoT: %s" % cmd.command)
	if cmd.command == "set_interval":
		if 'interval' not in cmd.data:
			print("Error: Interval was not present")
		else:
			waitInterval[0]=cmd.data['interval']
			print("Reporting interval changed to %f" % waitInterval[0])
	elif cmd.command == "print":
		if 'message' not in cmd.data:
			print("Error: message was not included in command")
		else:
			print("Message Received from Watson IoT: %s" % cmd.data['message'])
	elif cmd.command == "stop":
		os.exit(0)
	else:
		print("Error: Unrecognized command: %s" % cmd.command)


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

