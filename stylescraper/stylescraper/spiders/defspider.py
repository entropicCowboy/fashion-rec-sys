import scrapy
from stylescraper.items import StyleItem

class DefspiderSpider(scrapy.Spider):
    name = "defspider"
    #allowed_domains = ["www.google.com"]
    start_urls = ["https://aesthetics.fandom.com/wiki/List_of_Aesthetics#Aesthetics_by_Type"]

    def parse(self, response):
        tables = response.css("div.twocolumn")

        for table in tables:
            styles = table.css("li")
            for style in styles:
                #name = style.css("a").attrib["title"]
                relative_url = style.css("a").attrib['href']
                page_url = "https://aesthetics.fandom.com" + relative_url
                yield response.follow(page_url, callback= self.parse_page)
    
    def parse_page(self, response):
        style_item = StyleItem()
        name = response.css("span.mw-page-title-main::text").get()
        #sections = response.css("div.mw-parser-output")
        #descriptions = response.xpath("//h2[span[@id='Fashion']]/following::*/text()")
        #descriptions = response.xpath("//h2[span[@id='Fashion']]/following-sibling::*[preceding::div]/text()")
        #descriptions = response.xpath("//h2[span[@id='Fashion']]/following-sibling::*[preceding::div][preceding::h2]/text()")
        #descriptions = response.xpath("//h2[span[@id='Fashion']]/following::*[preceding::div][preceding::h2]/text()")
        desc_list = response.xpath("//*[preceding::h2[1][span[@id='Fashion']]]/text()")
        descriptions = []
        for desc in desc_list[:-3]:
            descriptions.append(desc.get())
        
        rel_aest_list = response.xpath("//div[@data-source='related_aesthetics']/descendant::*/text()")
        if rel_aest_list:
            rel_aesthetics = []
            for aesthetic in rel_aest_list[1:]:
                rel_aesthetics.append(aesthetic.get())

        key_colors = response.xpath("//div[@data-source='key_colours']/child::*/text()")
        if key_colors:
            key_colors = key_colors[1].get()

        brands = response.xpath("//div[@data-source='related_brands']/child::*/text()")
        if brands:
            brands = brands[1].get()

        style_item["name"] = name,
        style_item["descriptions"] = descriptions,
        style_item["rel_aesthetics"] = rel_aesthetics,
        style_item["key_colors"] = key_colors,
        style_item["brands"] = brands

        if descriptions:
            yield style_item
        
#        

