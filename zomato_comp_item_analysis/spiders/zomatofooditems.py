"""
This script is a Scrapy spider named 'zomatofooditems' designed to scrape menu data from Zomato's API.
It interacts with an external API to fetch competitor data, constructs API URLs for individual restaurants, 
and extracts menu details, including categories, item names, prices, ratings, and tags like "BESTSELLER."

Key functionalities:
1. Fetch competitor data from a database API.
2. Resolve Zomato short URLs to full API endpoints for restaurant menus.
3. Scrape menu details and metadata for further analysis.
4. Use retries and user-agent headers to handle network requests robustly.
"""

import scrapy  
import requests  
import json  
from zomato_comp_item_analysis.items import ZomatoFoodItem  
from requests.adapters import HTTPAdapter  
from requests.packages.urllib3.util.retry import Retry  
import time  
from datetime import datetime 

class ZomatofooditemsSpider(scrapy.Spider):
    name = "zomatofooditems"  
    allowed_domains = ["zomato.com"]  
    
    # custom_settings = {
    #     'ROTATING_PROXY_LIST': [
    #         "http://46.175.155.77:8800",
    #         "http://46.175.154.219:8800",
    #         "http://46.175.154.122:8800",
    #         "http://46.175.155.210:8800",
    #         "http://46.175.152.66:8800",
    #         "http://46.175.155.195:8800",
    #         "http://46.175.155.71:8800",
    #         "http://46.175.152.54:8800",
    #         "http://46.175.153.182:8800",
    #         "http://46.175.153.82:8800",
    #     ],
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    #         'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    #     },
    # }

    def start_requests(self):
        """
        Entry point for the spider.
        Fetches competitor data from a database API and constructs Zomato menu API URLs for each restaurant.
        """
        
        headers_query = 'SELECT * FROM restaverse_dev.competitor_master_data;'
        # use your own api to fetch resids
       
        response = requests.post(
            url="------",
            headers=headers,
            json={"query": headers_query}
        )

        try:
            
            data = response.json()
            self.logger.info("Fetched data: %s", data)
        except json.JSONDecodeError:
            
            self.logger.error("Failed to parse JSON response.")
            return

        if not isinstance(data, list):
            self.logger.error("Expected a list but got something else.")
            return

        
        session = requests.Session()
        retry_strategy = Retry(
            total=5,
            backoff_factor=1, 
            status_forcelist=[500, 502, 503, 504],  
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}

        
        for row in data:
            res_id = row.get("res_id") 
            if not res_id:
                continue

           
            short_url = f"https://zoma.to/r/{res_id}"
            try:
                expanded_response = session.get(short_url, headers=headers, allow_redirects=True, timeout=10)
                expanded_url = expanded_response.url
                path_part = "/".join(expanded_url.split("/", 3)[-1].split("/")[0:])
                api_url = f"https://www.zomato.com/webroutes/getPage?page_url=/{path_part}/order&location=&isMobile=0"
                self.logger.debug(f"API URL for res_id {res_id}: {api_url}")
            except requests.RequestException as e:
                self.logger.error(f"Error resolving URL for res_id {res_id}: {e}")
                continue

           
            yield scrapy.Request(
                url=api_url,
                callback=self.parse,
                headers={"User-Agent": user_agent},
                meta={
                    "proxy": "http://scrapeops.country=in:dbc08e8a-4f73-4088-9f13-c2db0a774557@residential-proxy.scrapeops.io:8181",
                    "competitor_id": row.get("competitor_id"),
                    "brand_name": row.get("brand_name"),
                    "city": row.get("city"),
                    "sub_zone": row.get("sub_zone"),
                    "res_id": res_id,
                    "platform": row.get("platform"),
                },
            )

            
            time.sleep(1)

    def parse(self, response):
        """
        Parses the JSON response from the Zomato menu API.
        Extracts menu details and metadata and yields them as structured items.
        """
        try:
            self.logger.debug(f"Received response for URL: {response.url}")
            data = json.loads(response.text)  
            menus = data.get("page_data", {}).get("order", {}).get("menuList", {}).get("menus", [])
            if not menus:
                self.logger.error("menus is missing or empty in the response")
                return

            
            meta_data = response.meta

            for menu_item in menus:
                menu = menu_item.get("menu", {})
                main_category = menu.get("name", "No Name Found")  
                categories = menu.get("categories", [])
                for category_wrapper in categories:
                    category = category_wrapper.get("category", {})
                    category_name = category.get("name", "No Category Name") 

                    items = category.get("items", [])
                    for item_wrapper in items:
                        item = item_wrapper.get("item", {})
                        item_name = item.get("name", "No Item Name")  
                        price = item.get("price", "No Price")  

                       
                        rating = item.get("rating")
                        if rating:
                            rating_value = rating.get("value", "No Rating")
                            rating_count_org = rating.get("total_rating_text", "No rating count")
                            rating_count = rating_count_org.split()[0]
                        else:
                            rating_value = ""
                            rating_count = ""

                       
                        tag_objects = item.get("tag_objects", [])
                        tag = next((obj.get("title", {}).get("text") for obj in tag_objects if obj.get("title", {}).get("text") == "BESTSELLER"), None)

                        
                        scraped_item = ZomatoFoodItem(
                            main_category=main_category,
                            category=category_name,
                            item_name=item_name,
                            price=price,
                            rating=rating_value,
                            rating_count=rating_count,
                            tag=tag,
                            date=datetime.now().strftime("%Y-%m-%d"),
                            competitor_id=meta_data["competitor_id"],
                            brand_name=meta_data["brand_name"],
                            city=meta_data["city"],
                            subzone=meta_data["sub_zone"],
                            res_id=meta_data["res_id"],
                            platform=meta_data["platform"],
                        )
                        yield scraped_item

        except json.JSONDecodeError:
            self.logger.error("Failed to parse JSON response.")
