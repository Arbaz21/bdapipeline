from kafka import KafkaProducer
import pandas as pd
import json
import time

# Kafka configuration
KAFKA_TOPIC = "ecommerce_data"
KAFKA_SERVER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Path to the dataset
file_path = "./datasets/Pakistan_Largest_Ecommerce_Dataset.csv"
chunk_size = 1000  # Adjust the chunk size as needed

def stream_data_to_kafka():
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            records = chunk.to_dict(orient="records")
            for record in records:
                producer.send(KAFKA_TOPIC, record)
            producer.flush()
            print(f"Sent {len(records)} records to Kafka.")
            time.sleep(1)  # Throttle ingestion if needed
    except Exception as e:
        print(f"Error during ingestion: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    print("Starting Kafka Producer...")
    stream_data_to_kafka()
    print("Data ingestion completed.")
