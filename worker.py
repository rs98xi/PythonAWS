import webcrawler  # this is my own py file
import utils  # this is my own python file
import pika
import json

"""
The logging file for master python file
"""
WORKER_LOG_FILE = "worker_log.txt"


def sites_callback(ch, method, properties, body):  # the parameters are needed for the callback itself, but are not used
    """
    This function is the callback for the rabbitMQ channel connection
    :param ch: god bless, not used
    :param method: god bless, not used
    :param properties: god bless, not used
    :param body: the message itself
    :return: nothing
    """

    """
    Body decoding and loading in a JSON
    """
    str_body = body.decode('utf-8')

    buff = json.loads(str_body)

    """
    Extracting the link and directory
    """
    directory, link = buff["dir"], buff["link"].lower()

    utils.report_message("Received command: [" + link + ", " + directory + "]", WORKER_LOG_FILE)

    """
    Small check for adult content, not influencing the result, all files are downloaded the same
    """
    if "google" in link or "facebook" in link or "youtube" in link:
        # this is here because i don't want to get banned for accessing adult content on work VPN :)
        """
        The download call for the parameters
        """
        webcrawler.download_website(link, directory, WORKER_LOG_FILE)

        utils.report_message("Downloaded link: " + link, WORKER_LOG_FILE)
    else:
        utils.report_message("Link blacklisted: " + link, WORKER_LOG_FILE)


def main():
    """
    This is the main function of the worker
    :return: nothing
    """

    """
    Cleaning up log files
    """
    utils.clean_up_logs(WORKER_LOG_FILE)

    """
    Creating rabbitMQ connection and callback
    """
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
