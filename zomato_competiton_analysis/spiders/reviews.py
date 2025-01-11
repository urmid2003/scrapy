import scrapy
import json
import os
import random
import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

class ReviewsSpider(scrapy.Spider):
   
    name = "reviews"
    allowed_domains = ["zomato.com"]

   
    output_file = "scraped_reviews.json"
    stop_threshold_days = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def start_requests(self):
        """
        Initialize the scraping process by fetching restaurant data
        and constructing the initial request for reviews.
        """
      
        headers_query = 'SELECT * FROM competitor_master_data;'

        
        response = requests.post(
            url="----",
            json={"query": headers_query}
        )
        data = response.json()

       
        for record in data:
            res_id = record["res_id"]
            meta = {
                "competitor_id": record["competitor_id"],
                "brand_name": record["brand_name"],
                "city": record["city"],
                "sub_zone": record["sub_zone"],
                "platform": record["platform"],
                "res_id": res_id,
            }
           
            url = f"https://www.zomato.com/webroutes/reviews/loadMore?sort=dd&filter=reviews-dd&res_id={res_id}&page=1"
            yield scrapy.Request(
                url,
                callback=self.parse_reviews,
                meta=meta,  
                dont_filter=True,  
                headers={"User-Agent": "Mozilla/5.0"},  
            )

    def parse_reviews(self, response):
        """
        Parse the reviews from the response and handle pagination.
        """
        meta = response.meta  
        self.logger.info(f"Meta data: {meta}")
        try:
           
            response_data = json.loads(response.text)
            reviews = response_data.get("entities", {}).get("REVIEWS", {})

            for review_id, review_data in reviews.items():
                review_text = review_data.get("reviewText", "")
                review_id = review_data.get("reviewId", "")
                rating = review_data.get("ratingV2", None)
                review_type = review_data.get("ratingV2Text", "")
                relative_date = review_data.get("timestamp", "")
                review_date = self.convert_date(relative_date)  
                if not review_date:
                    self.logger.info(f"Stopping for res_id: {meta['res_id']} due to unrecognized date format: {relative_date}.")
                    return
                review_date_obj = datetime.strptime(review_date, "%Y-%m-%d").date()
                today = datetime.today().date()
                stop_threshold = today - timedelta(days=self.stop_threshold_days)
                if review_date_obj <= stop_threshold:
                    self.logger.info(
                        f"Stopping for res_id: {meta['res_id']} as reviews are older than {self.stop_threshold_days} days."
                    )
                    return

                
                item = {
                    "review": review_text,
                    "review_id": review_id,
                    "rating": rating,
                    "review_type": review_type,
                    "review_date": review_date,
                    "competitor_id": meta["competitor_id"],
                    "brand_name": meta["brand_name"],
                    "city": meta["city"],
                    "sub_zone": meta["sub_zone"],
                    "platform": meta["platform"],
                    "res_id": meta["res_id"],
                }
                self.logger.info(f"Scraped item: {item}")
                yield item

           
            page_data = response_data.get("page_data", {}).get("sections", {}).get("SECTION_REVIEWS", {})
            current_page = page_data.get("currentPage", 1)
            total_pages = page_data.get("numberOfPages", 1)
            if current_page < total_pages:
                next_page = current_page + 1
                next_url = f"https://www.zomato.com/webroutes/reviews/loadMore?sort=dd&filter=reviews-dd&res_id={meta['res_id']}&page={next_page}"
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_reviews,
                    meta=meta,
                    headers={"User-Agent": "Mozilla/5.0"},
                )

        except json.JSONDecodeError:
            self.logger.error("Failed to parse JSON response.")

    def convert_date(self, relative_date):
        """
        Convert relative dates (e.g., '27 minutes ago', '2 hours ago') to absolute dates.
        """
        today = datetime.today()
        text_to_num = {
            "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
        }

        try:
            relative_date = relative_date.strip().lower()
            if relative_date == "yesterday":
                return (today - timedelta(days=1)).strftime("%Y-%m-%d")
            elif relative_date == "today":
                return today.strftime("%Y-%m-%d")
            elif "month" in relative_date:
                value = relative_date.split()[0]
                months = text_to_num.get(value, int(value) if value.isdigit() else None)
                return (today - relativedelta(months=months)).strftime("%Y-%m-%d")
            elif "day" in relative_date:
                value = relative_date.split()[0]
                days = text_to_num.get(value, int(value) if value.isdigit() else None)
                return (today - timedelta(days=days)).strftime("%Y-%m-%d")
            elif "hour" in relative_date:
                value = relative_date.split()[0]
                hours = text_to_num.get(value, int(value) if value.isdigit() else None)
                return (today - timedelta(hours=hours)).strftime("%Y-%m-%d")
            elif "minute" in relative_date:
                value = relative_date.split()[0]
                minutes = text_to_num.get(value, int(value) if value.isdigit() else None)
               
                adjusted_datetime = today - timedelta(minutes=minutes)
                return adjusted_datetime.strftime("%Y-%m-%d")
            elif "second" in relative_date:
                
                return today.strftime("%Y-%m-%d")
            else:
                self.logger.error(f"Unrecognized relative_date format: {relative_date}")
                return None
        except Exception as e:
            self.logger.error(f"Error parsing date: {relative_date}, error: {e}")
            return None
