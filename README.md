# realtime-analytics-production-monitoring
Realtime analytics project @IE, Group G: production monitoring is simulated via streaming data

# machine-sensor-monitoring

![Data Streaming Diagram](https://github.com/arifcanaksoy/realtime-analytics-production-monitoring/blob/master/influx_dash.png "Production Monitoring Dashboard")

![InfluxDB Dashboard](https://github.com/arifcanaksoy/realtime-analytics-production-monitoring/blob/master/data-arcihtecture.png "InfluxDB Dashboard")


### Before starting
Install required packages:
  - pip install kafka-python
  - pip install kafka-utils
  - pip install pyspark
  - pip install influxdb-client
 
[Download](https://kafka.apache.org/downloads.html) Kafka and un-tar it. (The version which i am using is 2.5.0)
```sh
$ tar -xzf kafka_2.12-2.5.0.tgz
```

[Download](https://spark.apache.org/downloads.html) Spark and un-tar it. (The version which i am using is 2.4.5)
```sh
$ tar -xzf spark-2.4.5-bin-hadoop2.7.tgz
```

Set Spark Home
```sh
$ export SPARK_HOME="/Users/YOURUSERNAME/Development/Tools/spark-2.4.5-bin-hadoop2.7"
$ export PATH="$SPARK_HOME/bin:$PATH"
```

To test pyspark, run in terminal
```sh
$ pyspark
```
you should see
```sh
   ____              __
  / __/__  ___ _____/ /__
 _\ \/ _ \/ _ `/ __/  '_/
/__ / .__/\_,_/_/ /_/\_\   version 2.4.5
   /_/
```
[Download](https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11) Spark Streaming Kafka Assembly jar (The version which i am using is 2.4.5). We will use it it to stream data from Kafka.
**Important:** The version must match with Spark


### Start Zookeper
switch to folder where you un-tar kafka_2.12-2.5.0 
```sh
$ bin/windows/zookeeper-server-start.bat config/zookeeper.properties
```

### Start Kafka Server
```sh
$ bin/windows/kafka-server-start.bat config/server.properties
```

### Create Topic "test"
```sh
$ bin/windows/kafka-console-producer.bat --bootstrap-server localhost:9092 --topic ProductionMonitoring
```

### (Optional) To Monitor Incoming Messages
```sh
$ bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic ProductionMonitoring --from-beginning
```

### Producing Messages
run producer.py from this repo to produce messages
```sh
$ python3 producer.py
```

### Streaming Data
run streamer.py to stream data from Kafka to influxDB via Spark
```sh
$ spark-2.4.5-bin-hadoop2.7/bin/spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.5.jar /Users/YOURUSERNAME/git/realtime-analytics-production-monitoring/src/steamer.py
```
