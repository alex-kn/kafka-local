from asyncio import ALL_COMPLETED
from pydoc_data.topics import topics
from confluent_kafka.admin import AdminClient, NewTopic
from concurrent import futures
import yaml
import argparse


def create_topics_if_not_exists(topic_list, bootstrap_server):
    admin_client = AdminClient(
        {
            "bootstrap.servers": bootstrap_server,
            "api.version.request": True,
        }
    )

    existing_topics = list(admin_client.list_topics().topics.keys())

    if existing_topics:
        print("Already existing topics: {}.".format(str(existing_topics)))
    new_topics = [topic for topic in topic_list if topic.topic not in existing_topics]
    print("Found {} new topics.".format(len(new_topics)))

    if new_topics:
        fs = admin_client.create_topics(new_topics)

        for topic, future in fs.items():
            try:
                future.result()
                print("Topic {} created.".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}.".format(topic, e))


def pretty_print(new_topic):
    print(
        "Found topic definition for {}:\n    Partitions: {}\n    Replication Factor: {}\n    Config:\n        {}".format(
            new_topic.topic,
            new_topic.num_partitions,
            new_topic.replication_factor,
            yaml.dump(new_topic.config, default_flow_style=False).replace(
                "\n", "\n        "
            ),
        )
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create kafka topics defined in a yaml file.")
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        required=True,
        help="Yaml file with topic definitions",
    )
    parser.add_argument(
        "-b",
        "--bootstrap-server",
        dest="bootstrap_server",
        default="localhost:9092",
        help="Broker URL",
    )
    args = parser.parse_args()

    with open(args.file, "r") as file:
        topics_config = yaml.load(file, Loader=yaml.FullLoader)

    default_def = topics_config["default"]
    default_config = default_def["config"]

    topic_list = []

    for topic_name, topic_def in topics_config["topics"].items():

        # merge defaults with topic definition
        topic_config = (
            {**default_config, **topic_def["config"]}
            if topic_def and "config" in topic_def
            else default_config
        )
        topic_def = {**default_def, **topic_def} if topic_def else default_def

        new_topic = NewTopic(
            topic=topic_name,
            num_partitions=topic_def["partitions"],
            replication_factor=topic_def["replication-factor"],
            config=topic_config,
        )
        pretty_print(new_topic)

        topic_list.append(new_topic)

    create_topics_if_not_exists(topic_list, args.bootstrap_server)
