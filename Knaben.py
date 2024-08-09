"""Knaben Database Yas

"""

from urllib.parse import urlencode
from datetime import datetime
from json import loads, dumps

from searx.utils import (
    eval_xpath_getindex,
    extract_text,
    get_torrent_size,
    int_or_zero,
)

# about
about = {
    "website": 'https://knaben.eu/',
    "wikidata_id": None,
    "official_api_documentation": "https://knaben.eu/api/v1/",
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

# engine dependent config
categories = ['files']
paging = True

# search-url
base_url = 'https://knaben.eu'
search_url = "https://api.knaben.eu/v1"

# Knaben specific type-definitions
search_types = {
    "files": None,
    "music": [1000000, 6007000],
    "videos": [2000000, 3000000, 6001000, 6002000, 6003000, 6004000, 6005000, 6008000 ]
}

# do search-request
def request(query, params):
    search_type = search_types.get(params["category"], None)
    size = 50
    hide_xxx = params["safesearch"] > 0
    hide_unsafe = params["safesearch"] > 1
    query = {
        "search_type": "100%",
        "search_field": "title",
        "query": query,
        "order_by": "seeders",
        "order_direction": "desc",
        "from": (params["pageno"] - 1) * size,
        "size": size,
        "hide_unsafe": hide_unsafe,
        "hide_xxx": hide_xxx
    }

    if search_type is not None:
        query["categories"] = search_type

    params['method'] = 'POST'
    params['url'] = search_url
    params["data"] = dumps(query)
    params['headers']['Content-Type'] = 'application/json'
    logger.debug("query_url --> %s", params['url'])
    return params


# get response from search-request
def response(resp):
    results = []

    search_res = loads(resp.text)

    for hit in search_res.get("hits", []):
        if hit["bytes"] == 0 or "link" not in hit:  # Small chance there is a miss in the indexing
            continue


        date_str = hit["date"]
        if date_str.count("-") > 2 or "+" in date_str:  # Sometimes the format includes timezone ...
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        else:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

        results.append(
            {
                'url': hit["details"],
                'title': hit["title"],
                'metadata': hit["category"],
                'seed': hit["seeders"],
                'leech': hit["peers"],
                'filesize': hit["bytes"],
                "publishedDate": date,
                'torrentfile': hit["link"],
                'magnetlink': hit["magnetUrl"],
                'template': 'torrent.html',
            }
        )

    return results

