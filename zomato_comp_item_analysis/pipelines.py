import json
import requests

class JsonWriterPipeline:
    def open_spider(self, spider):
        
        self.items = []

    def close_spider(self, spider):
       
        if not self.items:
            spider.logger.info('No items to send.')
            return

        data_to_send = {
            'data': self.items,
            'tableName': 'competitor_zomato_item_details',
            'database': 'dev'
        }

        #use your own heards and api key to dump data to db
        response = requests.post(
            url="------",
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
