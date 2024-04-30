# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : configure_rabbit_mq.py
# @Software: PyCharm


from dotenv import load_dotenv
import os
from fastapi import HTTPException
import pika

# Load environment variables
load_dotenv()

# Retrieve username and password from environment
rabbitmq_username = os.getenv("RABBITMQ_USERNAME")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")
rabbitmq_url = os.getenv("RABBITMQ_URL", "localhost")
rabbitmq_port = os.getenv("RABBITMQ_PORT", 5672)
rabbitmq_vhost = os.getenv("RABBITMQ_VHOST", "/")


def connect_to_rabbitmq():
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbitmq_url, rabbitmq_port, rabbitmq_vhost, credentials)
    )
    channel = connection.channel()
    return connection, channel


def publish_message(message, exchange_name='ingest_message'):
    """Publish a message to a fanout exchange in RabbitMQ, meaning, there will be multiple consumers (or subscribers)
    for the same mesage."""
    connection, channel = connect_to_rabbitmq()
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    try:
        channel.basic_publish(exchange=exchange_name,
                              routing_key='',  # Routing key is ignored by fanout exchanges
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # Make message persistent
                              ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(f"Published message to exchange '{exchange_name}': {message}")

    channel.close()
    connection.close()

