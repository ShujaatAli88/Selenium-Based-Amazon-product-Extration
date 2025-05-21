from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from constants import AmazonRequestConstants, XpathConstants
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4
from models import ValidateData
from airtable_manager import AirTableManager


class AmazonCrawler:
    def __init__(self):
        self.driver = None
        self.airtable_obj = AirTableManager()

    def get_driver(self):
        print("Setting Up The Selenium Driver.")
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Network.enable", {})

    def set_cookies(self):
        print("Setting The Cookies.")
        for name, value in AmazonRequestConstants.cookies.value.items():
            self.driver.execute_cdp_cmd(
                "Network.setCookie",
                {
                    "name": name,
                    "value": value,
                    "domain": ".amazon.com",
                    "path": "/",
                    "httpOnly": False,
                    "secure": True,
                    "sameSite": "Lax",
                },
            )
        print("Cookies Set Successfully.")

    def request_home_page(self):
        print("Requesting the Home Page.")
        self.driver.get("https://www.amazon.com")
        print(self.driver.title)
        if "Amazon" in self.driver.title:
            print("Request to The Home Page successfull.")
            return True
        else:
            print("Failed to load page")
            return False

    def get_search_field(self):
        try:
            print("Getting The Search Field. ")
            search_field = self.driver.find_element(
                By.XPATH, "//input[contains(@id,'twotabsearchtextbox')]"
            )
            search_button = self.driver.find_element(
                By.XPATH, "//input[contains(@id,'nav-search-submit-button')]"
            )

            if search_field:
                print("search field and search button Extrcated Successfully.")
                return search_field, search_button
            else:
                print(f"Error While Extracting Search field:{search_field}")
                return False
        except Exception as err:
            print(f"Error while getting the search field:{err}")
            return False

    def collect_product_cards(self):
        try:
            print("Extract The product Cards.")
            product_cards = self.driver.find_elements(
                By.XPATH, XpathConstants.product_cards.value
            )
            if product_cards:
                print("products Cards extracted Successfully.")
                return product_cards
            else:
                print("Failed to get product Cards.")
                return False
        except Exception as err:
            print(f"Error While Extrcating the product Cards:{err}")
            return False

    def parse_data(self, extracted_data):
        try:
            print("Validating The Data.")
            model_item = ValidateData(
                product_id=extracted_data["Product_id"],
                product_name=extracted_data["Product Name"],
                product_price=extracted_data["Product Price"],
                product_rating=extracted_data["Product_rating"],
                image_url=extracted_data["Image_URL"],
            )
            print("Data Model Validated Successfully.")
            return model_item
        except Exception as err:
            print(f"Error while Validating The Data:{err}")
            return False

    def snake_to_title(self, snake_str):
        return snake_str.replace("_", " ")

    def get_product_details(self, card):
        try:
            print("Getting The Product Details.")
            #wait for the whole page to load...
            product_elem = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH, XpathConstants.pagination_element.value))
            )

            product_elem = card.find_element(
                By.XPATH, XpathConstants.product_element.value
            )
            product_name = product_elem.get_attribute("aria-label")
            product_price = card.find_element(
                By.XPATH, XpathConstants.product_price.value
            ).get_attribute("innerHTML")
            product_rating = card.find_element(
                By.XPATH, XpathConstants.product_rating.value
            ).get_attribute("innerHTML")
            image_element = card.find_element(
                By.XPATH, XpathConstants.image_element.value
            )
            image_src = image_element.get_attribute("src")
            product_url_elem = card.find_element(By.XPATH,XpathConstants.product_url.value)
            product_href = product_url_elem.get_attribute("href")
            product_url = f"https://www.amazon.com{product_href}"

            extracted_data = {
                "Product_id": str(uuid4()),
                "Product Name": product_name.strip()
                if product_name
                else "Product Name Not Found",
                "Product Price": product_price.strip()
                if product_price
                else "Price not found!",
                "Product_rating": product_rating.strip()
                if product_rating
                else "Product rating not found",
                "Image_URL": image_src.strip() if image_src else "Image URL Not found.",
                "product url" : product_url.strip() if product_url else "product url not found."
            }
            model_item = self.parse_data(extracted_data)
            if not model_item:
                print(f"Could Not Validate The Model Data:{model_item}")
                return False

            model_dict = model_item.model_dump()

            data_dict = {
                self.snake_to_title(key): value for key, value in model_dict.items()
            }

            print("Calling The Upsert Method...")
            print(f"Transformed data_dict: {data_dict}")
            self.airtable_obj.upsert_data(data=data_dict)

            print(f"data extrated: {extracted_data}")
            return True
        except Exception as err:
            print(f"Error in Product details method:{err}")
            return False


def main():
    STATUS = True
    records_present = True
    next_button = None
    page_number = 1
    amazon_manager = AmazonCrawler()
    amazon_manager.get_driver()
    amazon_manager.set_cookies()
    home_page_respone = amazon_manager.request_home_page()
    if not home_page_respone:
        print(f"Home Page Request Returned:{home_page_respone}")
        STATUS = False
        return STATUS

    search_field, search_button = amazon_manager.get_search_field()
    if not search_field:
        print(f"get Search Field returned:{search_field}")
        STATUS = False
        return STATUS

    categores_to_process = AmazonRequestConstants.categories_to_process.value
    for catgory in categores_to_process:
        search_field.send_keys(catgory)
        search_button.click()

        cards = amazon_manager.collect_product_cards()
        if not cards:
            print(f"Cards collections failure:{cards}")
            STATUS = False
            return STATUS
        
        for card in cards:
            while records_present:#pagination...
                product_details_status = amazon_manager.get_product_details(card)
                if not product_details_status:
                    STATUS = False
                    continue

                next_button = WebDriverWait(amazon_manager.driver,10).until(
                    EC.element_to_be_clickable((By.XPATH, XpathConstants.next_page_button.value))
                )
                if next_button:
                    page_number += 1
                    print(f"More records available going to page number:{page_number}")
                    next_button.click()
                else:
                    print("No more pages available for this Category.")
                    next_button = False
                # break

        break
