import requests
from requests import ConnectionError, HTTPError, Timeout
import json
from bs4 import BeautifulSoup
import copy
from scrapper.headers_payload_etc import additional_features_dict
import logging
import re
import sys
from scrapper.helpers import find_number, find_floor

# logging configuration
logging.basicConfig(filename='../error_log.log',
                    format='%(asctime)s - %(levelname)s: \n- %(message)s',
                    level=logging.WARNING)


class RequestBs:
    """Creates request and BeautifulSoup objects"""

    def __init__(self, payload, request_headers, url, **kwargs):
        """Returns request object

        Keyword arguments:
            type -- type of estate (apartment, apartment-share, house, etc.)
            category -- buy or rent
            region -- region in which will search
        """

        self.bs = None

        if "type" in kwargs:
            payload["settings"]["Type"] = kwargs["type"]
        if "category" in kwargs:
            payload["settings"]["Category"] = kwargs["category"]
        if "region" in kwargs:
            payload["settings"]["Regions"].append(kwargs["region"])

        # set payload to easily set isRent or isSale property later
        self.payload = payload

        try:
            self.response = requests.post(url, data=json.dumps(payload), headers=request_headers)
        except (ConnectionError, HTTPError, Timeout) as e:
            logging.error(str(e) + ": " + self.__init__.__name__)
            sys.exit(1)

        # set count for the position so that next request fetches all the data
        self.payload["position"] = self.response.json()["Count"]

        try:
            self.response = requests.post(url, data=json.dumps(payload), headers=request_headers)
        except (ConnectionError, HTTPError, Timeout) as e:
            logging.error(str(e) + ": " + self.__init__.__name__)
            sys.exit(1)

        if self.response is not None:
            self.get_bs_object(method="post")

    def set_new_bs_object_get(self, url):
        try:
            self.response = requests.get(url)
        except (ConnectionError, HTTPError, Timeout) as e:
            logging.error(str(e) + ": " + self.set_new_bs_object_get.__name__)
            sys.exit(1)

        self.get_bs_object()

    def get_bs_object(self, method="get"):
        """Creates and returns BeautifulSoup object"""
        if self.response is None:
            return None

        # get the data from post
        if method == "post":
            rows = self.response.json()["Rows"]

            # remove escaped content just to be sure that bs gets the right data
            encoded_rows = bytes(rows, encoding='utf-8')
            escaped_rows = encoded_rows.decode('unicode-escape')

            self.bs = BeautifulSoup(escaped_rows, "html.parser")

        if method == "get":
            # get the data form get
            self.bs = BeautifulSoup(self.response.text, "html.parser")


class GetData:
    """Contains different methods for fetching various kind of data"""

    def __init__(self, json_template, rbs):
        self.json_templates_list = []
        self.rbs = rbs
        self.links = []

        # for testing
        self.testing = []

        # creates list of json templates to be filled with data
        # it has same number of elements as the number of links found
        for i in range(int(self.rbs.response.json()["Count"])):
            self.json_templates_list.append(copy.deepcopy(json_template))

    def get_links(self):
        """Sets all the links that are found for current selection"""

        for link in self.rbs.bs.findAll("a", {"class": "b"}):
            self.links.append(link["href"])

    def get_first_page_data(self):
        """Gets the data available on the search page and sets all the links found"""

        # set links for pages
        self.get_links()

        # get div with data about name, price, address, etc.
        # im for loop divs are with class 'a ax' that wraps the desired data
        for index, div in zip(range(len(self.json_templates_list)), self.rbs.bs.findAll("div", {"class": "a ax"})):

            # set isRent or isSale
            if self.rbs.payload["settings"]["Category"] == "1":
                self.json_templates_list[index]["isRent"] = True
            elif self.rbs.payload["settings"]["Category"] == "2":
                self.json_templates_list[index]["isSale"] = True

            # add links to origSource
            self.json_templates_list[index]["origSource"] = self.links[index]

            # get the name of the object
            try:
                name = div.h2.a.get_text()
                self.json_templates_list[index]['name'] = name
            except AttributeError as e:
                logging.error(self.json_templates_list[index]["origSource"] + str(e))

            # get the address and zip code
            try:
                div_street_zip = div.find('div', {'class': 'a ay'})
                street = bytes(div_street_zip.select('p')[0].get_text(), encoding='latin_1').decode('utf-8')

                zip_code = div_street_zip.select('p')[1].get_text().split(' ')[0]
            except AttributeError as e:
                logging.error(self.json_templates_list[index]["origSource"] + str(e))
                zip_code = 0
                street = ""

            self.json_templates_list[index]['address']['zipCode'] = zip_code
            self.json_templates_list[index]['address']['street'] = street

            # get space (number of m2) and floor
            div_m2 = div.find('div', {'class': 'a tc'})
            space_floor = div_m2.select('p')

            floor = 0

            if len(div_m2.select('p')) == 2:
                space = int(space_floor[1].get_text().split('m')[0])
            else:
                space = 0

            if space_floor[0].get_text().split('.')[0].isdigit():
                floor = int(space_floor[0].get_text().split('.')[0])

            self.json_templates_list[index]["mainFeatures"]["livingSpace"] = space
            self.json_templates_list[index]["mainFeatures"]["floor"] = floor

            try:
                # get total price
                price = div.find("h2", {"class": "a"}).get_text()
                price = re.findall("\d", price)
                self.json_templates_list[index]["price"]["rentPrice"] = int("".join(price))
            except (AttributeError, ValueError) as e:
                logging.error(self.json_templates_list[index]["origSource"] + " - " + str(e) +
                              "\n - " + self.get_first_page_data.__name__)
                self.json_templates_list[index]["price"]["rentPrice"] = 0

    def get_ad_page_data(self):
        """Sets the data about additional features (exterior, interior, etc.)"""

        for link in self.links:
            self.rbs.set_new_bs_object_get(link)

            current_json_template = None

            # select json template where to put the data
            for template in self.json_templates_list:
                if template["origSource"] == link:
                    current_json_template = template

            self.add_to_equipment(current_json_template)
            self.add_price_data(current_json_template)
            self.add_main_data(current_json_template)
            print("Current page: ", link)

    def add_price_data(self, current_template):
        """Adds data about price to the template"""

        # find div that wraps info about price
        div_price = self.rbs.bs.find("div", {"id": "xInfos"}).find("div", {"class": "a"})

        # get price
        extra_cost = div_price.select('div')[1].get_text()
        expenses = 0

        if re.match("Nebenkosten", extra_cost) or re.match("Extra cost", extra_cost):
            extra_cost = int("".join(re.findall('\d', extra_cost)))
            expenses = extra_cost
        else:
            logging.info(current_template["origSource"] + ": couldn't locate expenses")

        total_cost = current_template["price"]["rentPrice"]
        net_rent = total_cost - expenses
        current_template["price"]["expenses"] = expenses
        current_template["price"]["rentNetPrice"] = net_rent

    def add_main_data(self, current_template):
        """Adds data about space, floors, date available, etc."""
        div_wrapper = self.rbs.bs.find("div", {"id": "xInfos"}).find("li", {"class": "cb pt15"})
        data = []

        # get available data about object
        for div in div_wrapper.findAll("div", {"class": "cb"}):
            if div.get_text() != "":
                data.append(div.get_text())

        for d in data:

            if d is not None:
                d = d.strip()
                if re.match("Zimmer", d):
                    rooms = d.split()[1]
                    current_template["mainFeatures"]["rooms"] = rooms
                elif re.match("Etage", d) and not re.match("Etagen im Haus", d):
                    floor = find_floor(d)
                    if floor == 0:
                        floor = "ground floor"
                    current_template["mainFeatures"]["floor"] = floor
                elif re.match("Wohnfläche", d):
                    living_space = find_number(d)
                    current_template["mainFeatures"]["livingSpace"] = living_space
                elif re.match("Nutzfläche", d):
                    floor_space = find_number(d)
                    current_template["mainFeatures"]["floorSpace"] = floor_space
                elif re.match("Raumhöhe", d):
                    current_template["mainFeatures"]["roomHeight"] = ""
                elif re.match("Verfügbar", d):
                    date = d.split()[1]
                    if not date[0].isdigit():
                        # sofor, immediately
                        if date[0] == "s" or date[0] == "S":
                            date = "immediately"
                        else:
                            date = "By arangement"
                    current_template["details"]["availableAt"] = date
                elif re.match("Baujahr", d):
                    year = find_number(d)
                    current_template["details"]["builtAt"] = year
                elif re.match("Kubatur", d):
                    number = find_number(d)
                    current_template["mainFeatures"]["volume"] = number
                elif re.match("Letzte Renovation", d):
                    year_renovated = find_number(d)
                    current_template["details"]["renovatedAt"] = year_renovated
                elif re.match("Etagen im Haus", d):
                    number_of_floors = find_number(d)
                    current_template["mainFeatures"]["floors"] = number_of_floors

    def add_to_equipment(self, current_template):
        """Adds data about additional features (heating, exterior, interior, etc.) to template"""

        # get the div that wraps data about equipment (additional features)
        div = self.rbs.bs.find("div", {"class": "cb"}).find("div", {"class": "a d"})

        # check if div has heading named 'Ausstattung' or 'Equipment'
        try:
            if div.h2.get_text() == "Ausstattung" or div.h2.get_text() == "Equipment":

                uls = div.findAll('ul', {'class': 'pb15'})

                for u in uls:
                    eq = u.li.ul.children
                    for e in eq:
                        feature = e.get_text()[1:].strip()

                        if feature in additional_features_dict:

                            if additional_features_dict[feature]\
                                    in current_template["additionalFeatures"]["characteristics"]:
                                current_template["additionalFeatures"]["characteristics"][additional_features_dict[feature]] = True

                            elif additional_features_dict[feature] in current_template["additionalFeatures"]["equipment"]:
                                current_template["additionalFeatures"]["equipment"][additional_features_dict[feature]] = True

                            elif additional_features_dict[feature] in current_template["additionalFeatures"]["exterior"]:
                                current_template["additionalFeatures"]["exterior"][additional_features_dict[feature]] = True

                            elif additional_features_dict[feature] in current_template["additionalFeatures"]["interior"]:
                                current_template["additionalFeatures"]["interior"][additional_features_dict[feature]] = True

                            elif additional_features_dict[feature] in current_template["additionalFeatures"]["heating"]:
                                current_template["additionalFeatures"]["heating"][additional_features_dict[feature]] = True

                            elif additional_features_dict[feature] in current_template["additionalFeatures"]["energy"]:
                                current_template["additionalFeatures"]["energy"][additional_features_dict[feature]] = True
            else:
                logging.info(current_template["origSource"] + ": no data about additional features found")
        except AttributeError as e:
            logging.error(current_template["origSource"] + ' - ' + str(e) +
                          '\n - Error occurred at: ' + self.add_to_equipment.__name__)



