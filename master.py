import webcrawler  # this is my own py file
import utils  # this is my own python file
import pika
import os
import shutil
import json

"""
The logging file for master python file
"""
MASTER_LOG_FILE = "master_log.txt"


def clean_up_directory():
    """
    This function removes the existing directory and replaces it with a empty one

    :return: nothing
    """

    """
    Checking if the folder exists and deleting it if yes
    """
    if os.path.exists("sites"):
        shutil.rmtree("sites")

    """
    Creating the new and empty one
    """
    os.mkdir("sites")


def main():
    """
    This function is the main function for the master
    :return: nothing
    """

    """
    Cleaning up previous results
    """
    clean_up_directory()
    utils.clean_up_logs(MASTER_LOG_FILE)

    """
    Getting country list
    """
    country_list = webcrawler.get_site_countries(MASTER_LOG_FILE)

    """
    Creating the rabbitmq connection
    """
    connection = pika.BlockingConnection()
    channel = connection.channel()

    channel.queue_declare(queue='PythonMaster')

    """"
    Iterating the list of countries
    """
    for country in country_list:
        """
        Getting the list of sites for current country
        """
        site_list = webcrawler.get_site_names(country, MASTER_LOG_FILE)

        number_of_sites = len(site_list)

        """
        Creating the directory for current country
        """
        os.mkdir("sites\\" + country)

        """
        Iterating the list of websites
        """
        for second_it in range(number_of_sites):
            pair = [country, site_list[second_it]]
            print(pair)

            """
            Getting the file path for the current website
            """
            country_code = pair[0]
            link = pair[1]
            target_directory = os.path.join(os.getcwd(), "sites\\", country_code, link + ".html")

            """
            Creating the JSON message for the worker
            """
            message = {"dir": target_directory, "link": link}

            """
            Sending message to worker
            """
            channel.basic_publish(exchange='', routing_key='PythonMaster', body=json.dumps(message))

            utils.report_message("Sent [" + link + ", " + target_directory + "]", MASTER_LOG_FILE)

        utils.report_message("Country: " + country + " OK", MASTER_LOG_FILE)


    """
    This input is for blocking the master to force close the connection
    """
    blocker = input("Blocker master, enter any value to exit\n")

    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        utils.report_message('Interrupted', MASTER_LOG_FILE)
        exit(0)
