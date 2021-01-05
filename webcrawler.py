import urllib.request
import os


def download_website(link, target_directory):

    normalized_link = link
    if not link.startswith("https://www."):
        normalized_link = "https://www." + link

    site_handle = urllib.request.urlopen(normalized_link)
    site_data = site_handle.read()

    site_handle.close()

    with open(target_directory, "wb+") as file:
        file.write(site_data)
    print(link, "OK")


def get_site_countries():
    site = "https://www.alexa.com/topsites/countries/"

    site_handle = urllib.request.urlopen(site)
    site_data = site_handle.read()

    decoded_site_data = site_data.decode("utf8")
    site_handle.close()
    decoded_site_data = decoded_site_data.split("\n")

    country_list = []

    for it in range(len(decoded_site_data)):
        if '<a href="countries/' in decoded_site_data[it]:
            country = decoded_site_data[it].replace("/", '"').split('"')[2]
            country_list.append(country)

    return country_list


def get_site_names(country):
    site = "https://www.alexa.com/topsites/countries/" + country

    site_handle = urllib.request.urlopen(site)
    site_data = site_handle.read()

    decoded_site_data = site_data.decode("utf8")
    site_handle.close()
    decoded_site_data = decoded_site_data.split("\n")

    site_list = []

    for it in range(len(decoded_site_data)):
        if '<div class="td DescriptionCell">' in decoded_site_data[it]:
            site = decoded_site_data[it + 2].replace("<", ">").split(">")[2]
            site_list.append(site)

    return site_list


def main():
    country_code = "RO"

    print(get_site_countries())
    sites = get_site_names(country_code)

    for link in sites:
        target_directory = os.path.join(os.getcwd(), "sites\\", country_code, link + ".html")
        print(link)
        download_website(link, target_directory)


if __name__ == "__main__":
    main()
