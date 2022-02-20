FROM confluentinc/cp-kafka

# We only use this image for creating topics, so these can be ignored
ENV KAFKA_BROKER_ID=ignored
ENV KAFKA_ZOOKEEPER_CONNECT=ignored

RUN pip install confluent_kafka
