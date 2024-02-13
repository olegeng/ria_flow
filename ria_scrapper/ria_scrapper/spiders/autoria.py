import scrapy
import time
from logger_config import logger
from scrapy_splash import SplashRequest
from datetime import datetime

class AutoriaSpider(scrapy.Spider):
    logger.info('Spider is working')
    name = "autoria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/car/used"]
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(0.5))
                    
            show_phone = assert(splash:select("a.size14.phone_show_link.link-dotted.mhide"))
            show_phone:click()
            assert(splash:wait(0.5))
            but = assert(splash:select("#show-phone > div.show-phone-header > a"))
            but:click()
            return splash:html()
        end
    '''
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 360,  # Збільште час очікування до 120 секунд
    }
    links_r = []

    def single_parse(self, response):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        url = response.url
        car_name = response.xpath("//h3[@class='auto-content_title']/text()").get()
        car_price = response.xpath("//*[@id='showLeftBarView']/section[1]/div[1]/strong/text()").get().replace(' ', ).replace('$', '')
        odometer = f'{response.xpath("""//span[@class="size18"]/text()""").get()}000'
        user_name = response.xpath("//div[@class='seller_info_name bold'][1]/text()").get()
        phone_number = response.xpath("//*[@id='phonesBlock']/div/span/text()").get()
        image_url = response.xpath("//img[@class='outline m-auto'][1]/@src").get()
        images_count = response.xpath("//span[@class='count']/span[@class='mhide']/text()").get().split(' ')[1]
        car_number = response.xpath("//span[@class='state-num ua']/text()").get()
        vin_code = response.xpath("//span[@class='vin-code']/text()").get()
        datetime_found = datetime.now()
        yield {
            'Website URL': url,
            'Car Name': car_name,
            'Price': car_price,
            'Odometer': odometer,
            'User': user_name,
            'Phone number': phone_number,
            'Image url': image_url,
            'Num of images': images_count,
            'Car number': car_number,
            'VIN': vin_code,
            'Time': datetime_found,
        }
    
    def parse(self, response):
        lis = int(''.join(response.xpath("//span[@class='page-item mhide'][6]/a/text()").get().split(' ')))
        
        links = response.xpath("//a[@class='address']/@href").getall()
        self.links_r.extend(links)
        
        for page in range(2, lis+1):
            print(f'page {str(page)}')
            if page == 3:
                print('---------------------------')
                print(self.links_r)
                print(len(self.links_r))
                print('END')
                print('DIRECT')

                break
            else: 
                yield response.follow(url=f'{self.start_urls[0]}/?page={page+1}', callback=self.parse)
        if page==3:
            for item in self.links_r:
                print(f'scrapping page: {item}')
                yield SplashRequest(url=item, callback=self.single_parse, endpoint='execute',
                    args={'lua_source': self.script})
        
