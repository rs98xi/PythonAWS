import webcrawler  # this is my own py file
import utils  # this is my own python file
import pika

WORKER_LOG_FILE = "worker_log.txt"


def sites_callback(ch, method, properties, body):
    str_body = body.decode('utf-8')
    buff = str_body.split("~")
    directory, link = buff[0], buff[1].lower()

    utils.report_message("Received command: [" + link + ", " + directory + "]", WORKER_LOG_FILE)

    if "google" in link or "facebook" in link or "youtube" in link:
        # this is here because i don't want to get banned for accessing adult content on work VPN :)
        webcrawler.download_website(link, directory, WORKER_LOG_FILE)

        utils.report_message("Downloaded link: " + link, WORKER_LOG_FILE)
    else:
        utils.report_message("Link blacklisted: " + link, WORKER_LOG_FILE)


def main():
    utils.clean_up_logs(WORKER_LOG_FILE)

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
        utils.report_message('Interrupted', WORKER_LOG_FILE)
        exit(0)
