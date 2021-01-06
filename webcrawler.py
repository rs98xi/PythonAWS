import urllib.request
import urllib.error
import os
import utils  # my own py file

CRAWLER_LOG_FILE = "crawler_log.txt"


def download_website(link, target_directory, log_file):

    normalized_link = link
    if not link.startswith("https://www."):
        normalized_link = "https://www." + link

    site_handle = None

    try:
        site_handle = urllib.request.urlopen(normalized_link)
        site_data = site_handle.read()

        with open(target_directory, "wb+") as file:
            file.write(site_data)

        utils.report_message(link + " OK", log_file)

    except urllib.error.HTTPError:

        utils.report_message("Download failed: " + str(urllib.error.HTTPError) + link, log_file)

    finally:
        if site_handle is not None:
            site_handle.close()


def get_site_countries(log_file):
    site = "https://www.alexa.com/topsites/countries/"

    site_handle = None
    country_list = []

    try:

        site_handle = urllib.request.urlopen(site)
        site_data = site_handle.read()

        decoded_site_data = site_data.decode("utf8")
        site_handle.close()
        decoded_site_data = decoded_site_data.split("\n")

        for it in range(len(decoded_site_data)):
            if '<a href="countries/' in decoded_site_data[it]:
                country = decoded_site_data[it].replace("/", '"').split('"')[2]
                country_list.append(country)

        utils.report_message("Download successful: " + site, log_file)

    except urllib.error.HTTPError:

        utils.report_message("Download failed: " + str(urllib.error.HTTPError) + site, log_file)

    finally:
        if site_handle is not None:
            site_handle.close()

    return country_list


def get_site_names(country, log_file):
    site = "https://www.alexa.com/topsites/countries/" + country

    site_list = []
    site_handle = None

    try:
        site_handle = urllib.request.urlopen(site)
        site_data = site_handle.read()

        decoded_site_data = site_data.decode("utf8")
        site_handle.close()
        decoded_site_data = decoded_site_data.split("\n")

        for it in range(len(decoded_site_data)):
            if '<div class="td DescriptionCell">' in decoded_site_data[it]:
                site = decoded_site_data[it + 2].replace("<", ">").split(">")[2]
                site_list.append(site)

    except urllib.error.HTTPError:

        utils.report_message("Download failed: " + str(urllib.error.HTTPError) + site, log_file)

    finally:
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
