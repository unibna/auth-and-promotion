import os 
import sys
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(BASE_DIR).replace('app', '')
sys.path.append(APP_DIR)


from app.common.kafka import KafkaConnector


consumer = KafkaConnector.init_consumer()
topics = ["auth.login"]
consumer.subscribe(topics)
while True:
    msg = consumer.poll(1)
    if msg:
        print("-----> message")
        print("topic:", msg.topic())
        print("key:", msg.key().decode('utf-8'))
        print("value:", msg.value().decode('utf-8'))
