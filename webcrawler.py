import urllib.request


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


if __name__ == "__main__":
    print(get_site_countries())
    print(get_site_names("RO"))
