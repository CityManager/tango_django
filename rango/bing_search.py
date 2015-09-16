#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import json
import urllib
from urllib import parse, request
from urllib.error import URLError

__author__ = 'CityManager'

BING_API_KEY = r'mhOEWLS13CPb5pGPU/B25uzmMySy+WGGmj6wdFzEPsY'


def run_query(search_terms):
    # Bing 的搜索API地址
    root_url = r'https://api.datamarket.azure.com/Bing/Search/v1/'
    source = r'web'

    result_per_page = 10
    offset = 0

    query = "'{0}'".format(search_terms)
    query = urllib.parse.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        result_per_page,
        offset,
        query)

    username = ''

    password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    result = []

    try:
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        request.install_opener(opener)

        response = request.urlopen(search_url).read()
        print(response)

        json_response = json.load(response)

        print(json_response)
        result.append(json_response)

    except URLError as e:
        print("Error when querying the Bing API: ", e)

    return result


if __name__ == '__main__':
    run_query("百度")
