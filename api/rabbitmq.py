import json
from typing import Optional

import pika
from pydantic import BaseModel

import config

params = dict(config.get_env())


class QueueManager(BaseModel):

    """
    A class to manage queue for rabbitmq with pika
    ...

    Attributes
    ----------
    rabbitMQHost: str
        Host for the rabbitmq service
    ...
    Methods
    ----------

    publish_message():
        Publish message to an exchange
    """

    rabbitmq_host: Optional[str] = params["RABBITMQ_HOST"]

    async def publish_message(self, input_message: dict, exchange_ob: str) -> bool:

        """
        Publish message to an exchange
        ...

        Parameters
        ----------
        Just self

        Returns
        -------
        dict object
        Schema
            messageData: str
                message pulled from queue
        ...

        """

        # Establish connection with rabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_host)
        )
        channel = connection.channel()

        # Declare exchange
        channel.exchange_declare(exchange=exchange_ob, exchange_type="fanout")

        # Publish message to exchange
        channel.basic_publish(
            exchange=exchange_ob,
            routing_key="",
            body=json.dumps(input_message, default=str),
        )

        connection.close()

        return True
