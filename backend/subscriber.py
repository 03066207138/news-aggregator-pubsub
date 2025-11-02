import pika
import json

RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'topic_exchange'
EXCHANGE_TYPE = 'topic'

# List of queues (one per topic or any other custom logic)
QUEUES = ['sports', 'technology', 'business', 'health', 'politics', 'entertainment']

def create_queues():
    try:
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare an exchange (if not already created)
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)

        for queue_name in QUEUES:
            # Declare a queue for each topic
            channel.queue_declare(queue=queue_name, durable=True)

            # Bind each queue to the exchange with a routing key (topic)
            channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=queue_name)
            print(f"Queue '{queue_name}' created and bound to exchange '{EXCHANGE_NAME}'.")

        # Close the connection
        connection.close()

    except Exception as e:
        print(f"Error creating queues: {e}")
        raise e

# Function to consume messages from RabbitMQ (Subscriber)
def consume_messages():
    try:
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)

        for queue_name in QUEUES:
            # Declare and bind the queues
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=queue_name)
            print(f"Listening to queue '{queue_name}'.")

            def callback(ch, method, properties, body):
                message = json.loads(body)
                print(f"Received message from {queue_name}: {message}")
                ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

            # Start consuming messages from each queue
            channel.basic_consume(queue=queue_name, on_message_callback=callback)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as e:
        print(f"Error consuming messages: {e}")
        raise e

# Main function to set up queues and consumers
if __name__ == '__main__':
    # Create 6 queues
    create_queues()

    # Start consuming messages in the background (you can run this in a separate thread if needed)
    consume_messages()
