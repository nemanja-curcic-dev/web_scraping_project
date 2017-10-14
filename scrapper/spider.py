from scrapper.logic import RequestBs, GetData
from scrapper.headers_payload_etc import payload, request_headers, json_template

request_bs = RequestBs(payload, request_headers,
            'http://www.urbanhome.ch/Search/DoSearch',
            type="1", category="1", region="40")

get_data_object = GetData(json_template, request_bs)

get_data_object.get_first_page_data()
get_data_object.get_ad_page_data()