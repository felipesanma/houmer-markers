import json

import pika

from config import get_env, log
from data_processing import insert_houmer_activity

params = get_env()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=params["RABBITMQ_HOST"])
)
channel = connection.channel()
channel.exchange_declare(exchange=params["EXCHANGE"], exchange_type="fanout")
channel.queue_declare(queue=params["ACTIVITY_QUEUE"])
channel.queue_bind(exchange=params["EXCHANGE"], queue=params["ACTIVITY_QUEUE"])

log.info(" [*] Waiting for messages.")


def callback(ch, method, properties, body):
    log.info(" [x] Received %s" % body)
    json_message = json.loads(body.decode("utf-8"))
    insert_houmer_activity(json_message["houmer_id"])
    log.info(" [x] Done")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=params["ACTIVITY_QUEUE"], on_message_callback=callback, auto_ack=True
)
channel.start_consuming()
