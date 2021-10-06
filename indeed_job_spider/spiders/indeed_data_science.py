from scrapy import Spider
from scrapy.http import Request
import os
import glob
from datetime import datetime


class IndeedSpider(Spider):
    name = 'indeed_data_science'
    allowed_domains = ['indeed.com']
    start_urls = [
        'https://de.indeed.com/Jobs?q=Data+Science&l=Deutschland&fromage=last&sort=date']

    def parse(self, response):
        jobs = response.xpath(
            '//div[contains(@id, "mosaic-provider-jobcards")]/child::a/@href').extract()

        for job in jobs:
            absolute_job_url = response.urljoin(job)
            yield Request(absolute_job_url,
                          callback=self.parse_job)

        # next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        # if next_page:
        #     yield Request(next_page, self.parse)

    def parse_job(self, response):
        job_title = response.xpath(
            '//div[@class="jobsearch-JobInfoHeader-title-container "]/child::h1/text()').extract_first()

        job_description = response.xpath(
            '//div[@id="jobDescriptionText"]').extract()

        yield{
            'job_title': job_title,
            'job_description': job_description
        }

    def close(self, reason):
        # Save the file as .csv
        json_file = max(glob.iglob('*.json'), key=os.path.getctime)
        os.rename(
            json_file, f"./data/indeed_ds_{datetime.today().strftime('%Y-%m-%d')}.json")
