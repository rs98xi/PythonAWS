import webcrawler  # this is my own py file
import pika


def sites_callback(ch, method, properties, body):
    str_body = body.decode('utf-8')
    buff = str_body.split("~")
    directory, link = buff[0], buff[1].lower()

    print("Received command: [" + link + ", " + directory + "]")

    if "google" in link or "facebook" in link or "youtube" in link:
        webcrawler.download_website(link, directory)

        print("Downloaded link:", link)


def main():

    connection = pika.BlockingConnection()
    channel = connection.channel()

    channel.queue_declare(queue='PythonMaster')

    channel.basic_consume(queue='PythonMaster',
                          auto_ack=True,
                          on_message_callback=sites_callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)
