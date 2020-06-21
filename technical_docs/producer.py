# this script simulates data creation of machine sensor, as realtime

from time import sleep
from json import dumps
import random
from kafka import KafkaProducer

# configure KafkaProducer, define ports, host etc.
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
	value_serializer=lambda x: 
	dumps(x).encode('utf-8'))

# initial values
temperature = 160
pressure = 3.0
production = 1000
hygiene = 9.0
OEE = 85

# message to be sent to Kafka is initiated
messages = []

# increments values to pretend the data as alive
for i in range(500):
	value_random_T = random.choice([-1, +1, -0.5, +1.5])
	value_random_P = random.choice([-0.5, +0.3, +0.4])
	value_random_H = random.choice([-0.005, +0.005])
	value_random_O = random.choice([-0.05, +0.05])

	# create message line as key-value pairs
	messages.append({'oilTemp': temperature + value_random_T, 'pressure': pressure + value_random_P,
	 'hygieneFactor': hygiene + value_random_H, 'OEE': OEE + value_random_O,
	 'volumeProduced': production + 100})
	
	# in case print is needed to check format: print({'oilTemp': temperature + value_random_T, 'pressure': pressure + value_random_P, 'production': production + 100})
	temperature = temperature + value_random_T
	pressure = pressure + value_random_P
	hygiene = hygiene + value_random_H
	production = production + 25

# write the messages to Kafka line by line every 5 seconds
for msg in messages:
	producer.send('ProductionMonitoring', value=msg)
	# print(msg)
	sleep(5)

