import urllib.request
import urllib.error
import os
import utils  # my own py file

"""
The logging file for master python file
"""
CRAWLER_LOG_FILE = "crawler_log.txt"


def download_website(link, target_directory, log_file):
    """
    This function downloads a website html to a file
    :param link: The link to be downloaded
    :param target_directory: The file in which the website will be downloaded
    :param log_file: The log file to add messages
    :return: nothing
    """

    """
    Appending the corresponding beginning link
    """
    normalized_link = link
    if not link.startswith("https://www."):
        normalized_link = "https://www." + link

    site_handle = None

    try:
        """
        Opening the link and reading the content
        """
        site_handle = urllib.request.urlopen(normalized_link)
        site_data = site_handle.read()

        """
        Writing the html data to file as binary
        """
        with open(target_directory, "wb+") as file:
            file.write(site_data)

        """
        Message report
        """
        utils.report_message(link + " OK", log_file)

    except urllib.error.HTTPError:
        """
        Message report
        """
        utils.report_message("Download failed: " + str(urllib.error.HTTPError) + link, log_file)

    finally:
        """
        Closing the handle to the website
        """
        if site_handle is not None:
            site_handle.close()


def get_site_countries(log_file):
    """
    This function get the country codes from Alexa
    :param log_file: the logging file
    :return: a list of country codes
    """

    site = "https://www.alexa.com/topsites/countries/"

    site_handle = None
    country_list = []

    try:

        """
        Opening the link and reading the content
        """
        site_handle = urllib.request.urlopen(site)
        site_data = site_handle.read()

        """
        Decoding the html to string
        """
        decoded_site_data = site_data.decode("utf8")
        site_handle.close()
        decoded_site_data = decoded_site_data.split("\n")

        """
        Iterating the lines of the html to find key tags
        """
        for it in range(len(decoded_site_data)):
            """
            The tag we are looking for contains a country code
            After we get it, we append it to the list
            """
            if '<a href="countries/' in decoded_site_data[it]:
                country = decoded_site_data[it].replace("/", '"').split('"')[2]
                country_list.append(country)

        utils.report_message("Download successful: " + site, log_file)

    except urllib.error.HTTPError:
        """
        Message report
        """
        utils.report_message("Download failed: " + str(urllib.error.HTTPError) + site, log_file)

    finally:
        """
        Closing the handle to the website
        """
        if site_handle is not None:
            site_handle.close()

    return country_list


def get_site_names(country, log_file):
    """
    This function returns the top websites for a specific country
    :param country: the country to query
    :param log_file: the log file
    :return: a list of websites
    """
    site = "https://www.alexa.com/topsites/countries/" + country

    site_list = []
    site_handle = None

    try:
        """
        Opening the link and reading the content
        """
        site_handle = urllib.request.urlopen(site)
        site_data = site_handle.read()

        """
        Decoding the html to string
        """
        decoded_site_data = site_data.decode("utf8")
        site_handle.close()
        decoded_site_data = decoded_site_data.split("\n")

        """
        Iterating the lines of the html to find key tags
        """
        for it in range(len(decoded_site_data)):
            """
            The tag we are looking for contains a website
            After we get it, we append it to the list
            """
            if '<div class="td DescriptionCell">' in decoded_site_data[it]:
                site = decoded_site_data[it + 2].replace("<", ">").split(">")[2]
                site_list.append(site)

    except urllib.error.HTTPError:
        """
        Message report
        """
        utils.report_message("Download failed: " + str(urllib.error.HTTPError) + site, log_file)

    finally:
        """
        Closing the handle to the website
        """
        if site_handle is not None:
            site_handle.close()

    return site_list


def main():
    country_code = "RO"

    print(get_site_countries(CRAWLER_LOG_FILE))
    sites = get_site_names(country_code, CRAWLER_LOG_FILE)

    for link in sites:
        target_directory = os.path.join(os.getcwd(), "sites\\", country_code, link + ".html")
        print(link)
        download_website(link, target_directory, CRAWLER_LOG_FILE)


if __name__ == "__main__":
    main()
