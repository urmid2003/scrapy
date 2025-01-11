import json
import requests

class ZomatoCompetionAnalysisPipeline:
    def open_spider(self, spider):
       
        self.items = []

    def close_spider(self, spider):
        
        data_to_send = {
            'data': self.items,
            'tableName': 'competitor_zomato_reviews',
            'ignoreDuplicates': 1
        }
        
        #use your own heards and api key to dump data to db
        response = requests.post(
            url="",
            data=json.dumps(data_to_send),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            spider.logger.info('Data posted successfully.')
        else:
            spider.logger.error(f'Failed to post data: {response.status_code} - {response.text}')

    def process_item(self, item, spider):
       
        self.items.append(dict(item))
        return item
