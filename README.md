# Simple local broker setup for kafka

Quick and simple setup for a local Kafka cluster (single node) with AKHQ and automatic initial topic creation.

## Quickstart

1. Define topics in `topics.yml`. New topics are automatically created on startup.
2. Run `docker compose up -d` to launch zookeeper, kafka broker, akhq and inital topic creation.
3. Stop cluster with `docker compose down`.

## Topics

Topics are defined in `topics.yml` alongside their configuration. Topic configurations are merged with the default topic configuration and then created on the broker if they do not yet exist. Only new topics are created, existing topics are not deleted or altered.

Adding topics:

- Add topic to topics.yml
- Run `docker compose up -d` (Or restart the `init-topics` container manually)

Double check topic creations (and found topic definitions) in the logs of container `init-topics` running `docker logs init-topics`.

Topics are stored on volumes and remain across restarts. To start from scratch, volumes can be removed using `docker compose down -v`.

Browse topics with [AKHQ](https://github.com/tchiotludo/akhq) running on `localhost:8080`

## Access broker

The broker is avaliable on `localhost:9092`

Run `docker exec -it broker sh` to connect to the broker shell.
