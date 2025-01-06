from kafka import KafkaConsumer
import json

# Kafka configuration
KAFKA_TOPIC = "ecommerce_data"
KAFKA_SERVER = "kafka:9092"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"Subscribed to topic: {KAFKA_TOPIC}")

for message in consumer:
    print(f"Received message: {message.value}")
