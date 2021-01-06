import webcrawler  # this is my own py file
import utils  # this is my own python file
import pika
import os
import shutil
import json

MASTER_LOG_FILE = "master_log.txt"


def clean_up_directory():

    if os.path.exists("sites"):
        shutil.rmtree("sites")

    os.mkdir("sites")


def main():

    clean_up_directory()
    utils.clean_up_logs(MASTER_LOG_FILE)

    country_list = webcrawler.get_site_countries(MASTER_LOG_FILE)

    connection = pika.BlockingConnection()
    channel = connection.channel()

    channel.queue_declare(queue='PythonMaster')

    for country in country_list:
        site_list = webcrawler.get_site_names(country, MASTER_LOG_FILE)

        number_of_sites = len(site_list)

        os.mkdir("sites\\" + country)

        for second_it in range(number_of_sites):
            pair = [country, site_list[second_it]]
            print(pair)

            country_code = pair[0]
            link = pair[1]
            target_directory = os.path.join(os.getcwd(), "sites\\", country_code, link + ".html")
            # webcrawler.download_website(link, target_directory)

            message = {"dir": target_directory, "link": link}

            channel.basic_publish(exchange='', routing_key='PythonMaster', body=json.dumps(message))

            utils.report_message("Sent [" + link + ", " + target_directory + "]", MASTER_LOG_FILE)

        utils.report_message("Country: " + country + " OK", MASTER_LOG_FILE)

        break

    blocker = input("Blocker master, enter any value to exit\n")

    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        utils.report_message('Interrupted', MASTER_LOG_FILE)
        exit(0)
