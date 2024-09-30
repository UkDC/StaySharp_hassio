import pika, os

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
# url = os.environ.get('CELERY_BROKER_URL')
params = pika.URLParameters('amqps://cpqhujiw:j7WoBS4lDR345rsJmAsfgPP9Y1xbBzdK@woodpecker.rmq.cloudamqp.com/cpqhujiw')
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
channel.queue_declare(queue='hello')  # Declare a queue


def callback(ch, method, properties, body):
    print(" [x] Received " + str(body))


channel.basic_consume('hello',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
