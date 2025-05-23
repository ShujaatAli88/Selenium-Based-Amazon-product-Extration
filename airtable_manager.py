from pyairtable import Api
from config import Config
from constants import AirTableConstants
from log_handler import logger  # <-- Import logger


class AirTableManager:
    def __init__(self):
        self.api = Api(api_key=Config.AIRTABLE_API_KEY)
        self.base_id = Config.AIRTABLE_BASE_ID

    def upsert_data(self, *, data):
        logger.info("Upserting records into Air Table.")
        table = self.api.table(
            base_id=self.base_id, table_name=AirTableConstants.TABLE_NAME.value
        )
        table.batch_upsert(records=[dict(fields=data)], key_fields=["product id"])
        logger.info("Records Upserted Successfully.")

    def fetch_data(self, product_price):
        """
        Fetch all records where 'product price' matches the given value.
        """
        try:
            table = self.api.table(
                base_id=self.base_id, table_name=AirTableConstants.TABLE_NAME.value
            )
            formula = f"{{product price}} = '{product_price}'"
            records = table.all(formula=formula)
            logger.info(
                f"Fetched {len(records)} records for product price: {product_price}"
            )
            return [record["fields"] for record in records]
        except Exception as e:
            logger.error(f"Error fetching records: {e}")
            return []

    def fetch_one(self, product_price):
        """
        Fetch the first record where 'product price' matches the given value.
        Returns the fields dict or None if not found.
        """
        try:
            table = self.api.table(
                base_id=self.base_id, table_name=AirTableConstants.TABLE_NAME.value
            )
            formula = f"{{product price}} = '{product_price}'"
            records = table.all(formula=formula, max_records=1)
            if records:
                logger.info(f"Fetched one record for product price: {product_price}")
                return records[0]["fields"]
            logger.info(f"No record found for product price: {product_price}")
            return None
        except Exception as e:
            logger.error(f"Error fetching record: {e}")
            return None


#### Example Usage #####
if __name__ == "__main__":
    ob = AirTableManager()
    results = ob.fetch_one("$19.99")
    logger.info(f"Fetched records: {results}")
