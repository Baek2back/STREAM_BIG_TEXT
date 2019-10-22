# pip install pika

import pika

userid = "root";
password = "root";

credentials = pika.PlainCredentials(userid,password)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    return n


def on_request(ch, method, props, body):
    n = str(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()