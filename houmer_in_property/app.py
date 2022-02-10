import json

import pika

from config import get_env, log
from data_processing import (
    insert_houmer_in_property,
    insert_houmer_in_property_activity,
)

params = get_env()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=params["RABBITMQ_HOST"])
)
channel = connection.channel()
channel.exchange_declare(exchange=params["EXCHANGE"], exchange_type="fanout")
channel.queue_declare(queue=params["IN_PROPERTY"])
channel.queue_bind(exchange=params["EXCHANGE"], queue=params["IN_PROPERTY"])

log.info(" [*] Waiting for messages.")


def callback(ch, method, properties, body):
    log.info(" [x] Received %s" % body)
    json_message = json.loads(body.decode("utf-8"))
    insert_houmer_in_property(
        json_message["houmer_id"],
        float(params["RADIUS_LIMIT"]),
        float(params["MAX_DISTANCE"]),
    )
    insert_houmer_in_property_activity(json_message["houmer_id"])

    log.info(" [x] Done")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=params["IN_PROPERTY"], on_message_callback=callback, auto_ack=True
)
channel.start_consuming()
