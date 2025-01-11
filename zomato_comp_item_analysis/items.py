import scrapy


class ZomatoFoodItem(scrapy.Item):
    main_category = scrapy.Field()
    category = scrapy.Field()
    item_name = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    rating_count= scrapy.Field()
    tag = scrapy.Field()
    date= scrapy.Field()
    competitor_id = scrapy.Field()
    brand_name = scrapy.Field()
    city = scrapy.Field()
    subzone= scrapy.Field()
    res_id = scrapy.Field()
    platform = scrapy.Field()
