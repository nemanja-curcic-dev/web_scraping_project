from scrapper.logic import RequestBs, GetData
from scrapper.headers_payload_etc import payload, request_headers, json_template

request_bs = RequestBs(payload, request_headers,
            'http://www.urbanhome.ch/Search/DoSearch',
<<<<<<< HEAD
            type="1", category="1")
=======
            type="1", category="1", region="188542")

>>>>>>> description
get_data_object = GetData(json_template, request_bs)

get_data_object.get_first_page_data()
get_data_object.get_ad_page_data()

<<<<<<< HEAD
print(set(get_data_object.testing))

for d in get_data_object.json_templates_list:
    print(d)
=======
file_to_write = open('../data.txt', "w")

for d in get_data_object.json_templates_list:
    file_to_write.write(str(d) + "\n")

file_to_write.close()
>>>>>>> description
