""" File contains class Scraper which scrapes website https://www.hyperia.sk/ for info about job offerings
    Author: Adam Fabo
    Date: 23.8.2022
"""

import requests
from lxml import html

class Scraper:

    web_link = 'https://www.hyperia.sk/'

    # paths for each important element on site
    place_xpath = '/html/body/div/div/div/div/section[1]/div[2]/div/div/div[1]/p/text()'
    salary_xpath = '/html/body/div/div/div/div/section[1]/div[2]/div/div/div[2]/p/text()'
    contract_type_xpath = '/html/body/div/div/div/div/section[1]/div[2]/div/div/div[3]/p/text()'

    # contact email can have 2 different paths
    contact_email_xpath   = '/html/body/div/div/div/div/section[2]/div[2]/a'
    contact_email_xpath_2 = '/html/body/div/div/div/div/div[6]/a'


    def __init__(self,jobs):
        self.jobs = jobs

    def scrape(self):

        final_jobs = []

        for job in self.jobs.getchildren():

            title = job.getchildren()[0].text

            link_to_job = job.getchildren()[2][0].get('href')

            # load page of current job offering
            response = requests.get(self.web_link + link_to_job, stream=True)
            if not response.ok:
                continue

            response.encoding = response.apparent_encoding
            tree = html.document_fromstring(response.text)

            place         = tree.xpath(self.place_xpath)[0]
            salary        = tree.xpath(self.salary_xpath)[0]
            contract_type = tree.xpath(self.contract_type_xpath)[0]

            # try one path, if it is empty try another
            contact_email = tree.xpath(self.contact_email_xpath)
            if not contact_email:
                contact_email = tree.xpath(self.contact_email_xpath_2)

            contact_email = contact_email[0].get("href")
            contact_email = contact_email.replace("mailto:", "")

            job_info = {"title" : title, "place" : place, "salary" : salary, "contract_type" : contract_type, "contact_email" : contact_email}

            final_jobs.append(job_info)

        return final_jobs










