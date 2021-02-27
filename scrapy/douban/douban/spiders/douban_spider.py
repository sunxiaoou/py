import scrapy
from ..items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # print(response.text)
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] =\
                i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = \
                i_item.xpath(".//div[@class='hd']/a/span[1]/text()").extract_first()
            content =\
                i_item.xpath(".//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = ''.join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] =\
                i_item.xpath(".//div[@class='star']//span[2]/text()").extract_first()
            douban_item['evaluate'] =\
                i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] =\
                i_item.xpath(".//div[@class='bd']//span[@class='inq']/text()").extract_first()

            # print(douban_item)
            yield douban_item

            next_link = response.xpath("//span[@class='next']/link/@href").extract()
            if next_link:
                next_link = next_link[0]
                yield scrapy.Request('https://movie.douban.com/top250' + next_link,
                                     callback=self.parse)
