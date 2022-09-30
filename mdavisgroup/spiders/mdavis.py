import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://bid.mdavisgroup.com/lots?term={}&page=1&pageSize=60'

class MdavisSpider(scrapy.Spider):
    name = 'mdavis'
    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), cb_kwargs={'index':index})

    def parse(self, response, index):
        total_pages = response.xpath("//div[@class='ui mini pagination menu mobile hidden']/a[last()-1]/text()").get()
        current_page =response.xpath("//a[@class='item active']/text()").get()  
         
        link = response.url
       
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    link = link.replace(min,max)                                                                
                    yield response.follow(link, cb_kwargs={'index':index})

        links = response.css(".lot-grid-header::attr(href)")
        images = response.css("[name='lot-image']::attr(src)").getall()
        counter = 0
        for link in links:
            image = images[counter]
            yield response.follow("https://bid.mdavisgroup.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index, 'image':image})  
            counter = counter+1
    def parse_item(self, response, index, image): 
        print(".................")  
        product_url = response.url
        print(product_url)
        image = image
        print(image)       
        auction_date = response.xpath("//div[2]/span[@class='sale-date']/text()").get()
        print(auction_date)
        location = response.xpath("//div[@class='ui grid segment']/div[4]/text()").get()
        print(location)
        product_name = response.xpath("//a[@class='header']//text()").get()
        print(product_name)
        lot = response.xpath("//div[@class='ui header text-align-center']/text()[2]").get()        
        lot_number = lot.strip()
        ner1 = response.css('a.sub.header::text').get()
        ner2 = ner1.split('-')
        ner3 = ner2[0]
        ner4 = ner3.split(':')
        auctioner = ner4[1].strip()
        print(auctioner)

        des = response.xpath("//div[@data-tab='description']/text()").get()
        description = des.strip()
        print(description)
        
        yield{
            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : 'mdavisgroup',
            'description' : description             
        }