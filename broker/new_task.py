import sys
import pika, os

params = pika.URLParameters('amqps://cpqhujiw:j7WoBS4lDR345rsJmAsfgPP9Y1xbBzdK@woodpecker.rmq.cloudamqp.com/cpqhujiw')
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print (" [x] Sent %r" % (message,))