import webcrawler  # this is my own py file
import pika
import os
import shutil


def clean_up_directory():
    if os.path.exists("sites"):
        shutil.rmtree("sites")

    os.mkdir("sites")


def main():

    clean_up_directory()

    country_list = webcrawler.get_site_countries()

    connection = pika.BlockingConnection()
    channel = connection.channel()

    channel.queue_declare(queue='PythonMaster')

    for country in country_list:
        site_list = webcrawler.get_site_names(country)

        number_of_sites = len(site_list)

        os.mkdir("sites\\" + country)

        for second_it in range(number_of_sites):
            pair = [country, site_list[second_it]]
            print(pair)

            country_code = pair[0]
            link = pair[1]
            target_directory = os.path.join(os.getcwd(), "sites\\", country_code, link + ".html")
            # webcrawler.download_website(link, target_directory)

            message = target_directory + '~' + link
            channel.basic_publish(exchange='', routing_key='PythonMaster', body=message)

            print("Sent [" + link + ", " + target_directory + "]")

        print("Country:", country, "OK")

    blocker = input("Blocker master, enter any value to exit\n")

    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)
