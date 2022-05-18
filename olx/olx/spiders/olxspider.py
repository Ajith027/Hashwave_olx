import json
import scrapy
from scrapy.crawler import CrawlerProcess


class Olx(scrapy.Spider):
    name = 'sel'
    url = 'https://www.olx.in/api/relevance/v2/search?category=1723&facet_limit=100&lang=en-IN&location=4058877&location_facet_limit=20&platform=web-desktop&size=40&user=180c6963327xdcaea81'

    def start_requests(self):
        for page in range(0, 500):
            yield scrapy.Request(url=self.url + '&page=' + str(page),  callback=self.parse)

    def parse(self, response):
        data = response.text
        data=json.loads(data)

        for i in data['data']:
            id= i['id']
            yield scrapy.Request('https://www.olx.in/item/1bhk-luxury-branded-flat-for-rent-near-metro-cardiac-hospital-calicut-iid-'+id,callback=self.parse_item)

    def parse_item(self, response):

        items ={
            'name': response.css('h1._3rJ6e::text').get(),
            'id': response.css('div.fr4Cy strong::text')[-1].get(),
            'breadcrumbs': response.css('a._3C_pO::text').getall(),
            'price': response.css('span._2xKfz::text').get(),
            'image_url': response.css('img._39P4_').attrib['src'],
            'description': response.css('div.rui-2CYS9._31p_I p::text').get(),
            'seller_name': response.css('div._3oOe9::text').get(),
            'location': response.css('span._2FRXm::text').get(),
            'property_type': response.css('span._2vNpt::text').get(),
            'bathrooms': response.css('span._2vNpt::text')[1].get(),
            'bedrooms': response.css('span._2vNpt::text')[2].get()

        }

        data=json.dumps(items,indent=4)
        with open('Olx.json','a+') as json_file:
            json_file.write(data +'\n')


process = CrawlerProcess()
process.crawl(Olx)
process.start()
