from pyairtable import Api
from config import Config
from constants import AirTableConstants

class AirTableManager():
    def __init__(self):
        self.api = Api(api_key=Config.AIRTABLE_API_KEY)
        self.base_id = Config.AIRTABLE_BASE_ID

    def upsert_data(self,* , data):
        print("Upserting records into Air Table.")
        table = self.api.table(base_id=self.base_id,table_name=AirTableConstants.TABLE_NAME.value)
        table.batch_upsert(
            records=[dict(fields = data)],
            key_fields = ['product id']
        )
        print("Records Upserted Successfully.")


#### Example Usage #####
if __name__ == "__main__":
    ob = AirTableManager()
    ob.upsert_data(
        data = {
            "product id" : "1",
            "product name": "jako",
            "product price": "okkk",
            "product rating" : "2.2",
            "image url" : "https:ok.com"
        }
    )