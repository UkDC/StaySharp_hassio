
import pika, os

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
# url = os.environ.get('CELERY_BROKER_URL')
params = pika.URLParameters('amqps://cpqhujiw:j7WoBS4lDR345rsJmAsfgPP9Y1xbBzdK@woodpecker.rmq.cloudamqp.com/cpqhujiw')
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello CloudAMQP!')

print(" [x] Sent 'Hello World!'")
connection.close()
