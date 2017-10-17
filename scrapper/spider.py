#!/usr/bin/env python
#  -*- encoding: utf8 -*-


from logic import RequestBs, GetData
from headers_payload_etc import payload, request_headers, json_template

# create request
request_bs = RequestBs(payload, request_headers,
            'http://www.urbanhome.ch/Search/DoSearch',
            type="1", category="1", region="188542")

get_data_object = GetData(json_template, request_bs)

# get the data
get_data_object.get_first_page_data()
get_data_object.get_ad_page_data()

# write data to file
file_to_write = open('../data.txt', "w")

for d in get_data_object.json_templates_list:
    file_to_write.write(str(d) + "\n")

file_to_write.close()

