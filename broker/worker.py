import time
import pika, os

params = pika.URLParameters('amqps://cpqhujiw:j7WoBS4lDR345rsJmAsfgPP9Y1xbBzdK@woodpecker.rmq.cloudamqp.com/cpqhujiw')
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
channel.queue_declare(queue='hello')  # Declare a queue


def callback(ch, method, properties, body: str):
    print(" [x] Received %r" % (body,))
    time.sleep(str(body).count('.'))
    print(" [x] Done")


channel.basic_consume('hello',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
