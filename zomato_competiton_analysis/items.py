import scrapy


class ZomatoCompetitionAnalysisItem(scrapy.Item):
    # Define the fields for your item
    restaurant_name = scrapy.Field()
    review = scrapy.Field()
    review_id= scrapy.Field()
    rating = scrapy.Field()
    review_date = scrapy.Field()
    reviewer_name = scrapy.Field()
    review_type = scrapy.Field()
    competitor_id = scrapy.Field()
    brand_name = scrapy.Field()
    city = scrapy.Field()
    sub_zone = scrapy.Field()
    platform = scrapy.Field()
    res_id = scrapy.Field()
