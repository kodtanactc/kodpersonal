#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import redis
from setenv import RedisPwd

######  MQTT broker  ######

BrokerAddress = "test.mosquitto.org"    # Cloud MQTT
MqttTopic = "p4p"


######  Redis key reset  ######

RedisKey = 0


######  RedisHost info   ######

RedisHost = "redis-13849.c9.us-east-1-4.ec2.cloud.redislabs.com"  
RedisPort = "13849"

######  functions   ######

def check_db():
    ### Check Redis connection 
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    print("Connected Radis...: " + RedisHost)
    ### Check Redis Key
    ret = r.get(RedisKey)
    print (ret)                             ### for debug
    if ret is None:                         # if no exist RedisKey                 
        print("Failed Key")
        return ret                          # Return Value
    msg = str(ret.decode("utf-8"))
    print("RedisKey:" + RedisKey + " KeyValue:" + msg)
    return ret

### Redis data and number set 
def set_db(msg):                            ### set data to Redis
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    global RedisKey
    RedisKey += 1
    r.set(RedisKey ,msg)                   
    print("Updated Radis db=0")

def on_message(client, userdata, message):  ### callback when get message from MQTT broker
    msg = str(message.payload.decode("utf-8"))
    print("Message received:" + msg)
    set_db(msg)                             ### call Function set_db(msg)


######  Main   #######

### check
ret = check_db()
if ret is None:                             # for debug                 
    print("***** debug *****")

### Connect MQTT broker 
print("Connecting to MQTT broker:" + BrokerAddress)
client = mqtt.Client()               # Create new instance with Any clientID
client.on_message=on_message         # Attach function to callback
try:
    client.connect(BrokerAddress)    #connect to broker
except:
    print("***** Broker connection failed *****")
    exit(1) 

### Subscribe ###
print("Subscribe topic:", MqttTopic)
client.subscribe(MqttTopic)          # Subscribe MQTT

### loop forever to wait a message ###
print("Waiting message...")
client.loop_forever()                # Loop forever

