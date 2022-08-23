#!/usr/bin/env python3

""" Script downloads info about job offerings in site https://www.hyperia.sk/kariera/
    Author: Adam Fabo
    Date: 23.8.2022
"""

import requests
import json
from lxml import html
from scraper import Scraper



def main():

    jobs_xpath = '/html/body/div/div/div/div/div[2]/section/div/div[2]'

    response = requests.get('https://www.hyperia.sk/kariera/',stream=True)
    if not response.ok:
        exit(1)

    response.encoding = response.apparent_encoding
    tree = html.document_fromstring(response.text)

    # search for the div with job offers
    jobs = tree.xpath(jobs_xpath)
    if not jobs:
        exit(1)

    # create scraper and pass it the job tree
    scraper = Scraper(jobs[0])
    result = scraper.scrape()

    print(result)

    json_object = json.dumps(result, indent=4, ensure_ascii=False)

    with open("jobs.json", "w") as outfile:
        outfile.write(json_object)



if __name__ == "__main__":
    main()




