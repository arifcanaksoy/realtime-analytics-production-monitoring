from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import time
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# necessary fields to write data to influxDB
INFLUX_TOKEN = "your_token"
INFLUX_CLOUD_URL = "https://cloud_url_provided_by_influx.com"
INFLUX_ORGANIZATION_ID = "your_org_id"
INFLUX_BUCKET_ID = "your_bucket_id"

client = InfluxDBClient(url=INFLUX_CLOUD_URL, token=INFLUX_TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)

# spark functionalities and write message to influxDB
def printAndStoreMessage(msg):
	fluxData = "myMeasurement,host=myHost oilTemp=" + str(msg['oilTemp']) + ",pressure=" + str(msg['pressure']) + ",hygieneFactor=" + str(msg['hygieneFactor']) + ",OEE=" + str(msg['OEE']) + ",volumeProduced=" + str(msg['volumeProduced']) + " " + str(int(time.time_ns()))
	print(fluxData)
	write_api.write("6a68e3858308b63a", "94185f98c4f4fb4c", fluxData)
	return msg

sc = SparkContext(appName="PythonSparkStreamingKafka")
sc.setLogLevel("WARN")

ssc = StreamingContext(sc, 5)

kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'ProductionMonitoring', {'ProductionMonitoring':1})

# spark functionalities to attain a proper table
parsed = kafkaStream.map(lambda v: json.loads(v[1]))
parsed.count().map(lambda x: '# of data in this batch: %s' % x).pprint()
parsed.map(lambda x: printAndStoreMessage(x)).pprint()

# initiate the streaming
ssc.start()
ssc.awaitTermination()
