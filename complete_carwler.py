from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from constants import AmazonRequestConstants, XpathConstants
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4
from models import ValidateData
from airtable_manager import AirTableManager
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class AmazonCrawler:
    def __init__(self):
        self.driver = None
        self.airtable_obj = AirTableManager()

    def get_driver(self):
        print("Setting Up The Selenium Driver.")
        options = Options()
        # Set headless and other required flags
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # ✅ Create a unique temp user-data-dir to avoid conflicts
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_dir}")
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
            print("Request to The Home Page successful.")
            return True
        else:
            print("Failed to load page")
            return False

    def get_search_field(self):
        try:
            print("Getting The Search Field.")
            search_field = self.driver.find_element(
                By.XPATH, "//input[contains(@id,'twotabsearchtextbox')]"
            )
            search_button = self.driver.find_element(
                By.XPATH, "//input[contains(@id,'nav-search-submit-button')]"
            )

            if search_field and search_button:
                print("Search field and search button extracted successfully.")
                return search_field, search_button
            else:
                print("Error While Extracting Search field or button.")
                return False
        except Exception as err:
            print(f"Error while getting the search field: {err}")
            return False

    def collect_product_cards(self):
        try:
            print("Extracting the product cards.")
            product_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, XpathConstants.product_cards.value)
                )
            )
            if product_cards:
                print(f"{len(product_cards)} product cards extracted successfully.")
                return product_cards
            else:
                print("Failed to get product cards.")
                return False
        except Exception as err:
            print(f"Error while extracting the product cards: {err}")
            return False
        
    def scroll_page(self,scroll_pause_time=1):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(3):  # Scroll multiple times to ensure lazy-load triggers
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def parse_data(self, extracted_data):
        try:
            print("Validating the data.")
            model_item = ValidateData(
                product_id=extracted_data["Product_id"],
                product_name=extracted_data["Product Name"],
                product_price=extracted_data["Product Price"],
                product_rating=extracted_data["Product_rating"],
                image_url=extracted_data["Image_URL"],
            )
            print("Data model validated successfully.")
            return model_item
        except Exception as err:
            print(f"Error while validating the data: {err}")
            return False

    def snake_to_title(self, snake_str):
        return snake_str.replace("_", " ")

    def get_product_details(self, card):
        try:
            print("Getting the product details.")
            product_elem = card.find_element(
                By.XPATH, XpathConstants.product_element.value
            )
            product_name = product_elem.get_attribute("aria-label")

            product_price = "Price not found!"
            try:
                product_price = card.find_element(
                    By.XPATH, XpathConstants.product_price.value
                ).get_attribute("innerHTML")
            except Exception as err:
                print(f"Error while finding product price:{err}")

            product_rating = "Product rating not found"
            try:
                product_rating = card.find_element(
                    By.XPATH, XpathConstants.product_rating.value
                ).get_attribute("innerHTML")
            except Exception as err:
                print(f"Error while finding product rating:{err}")

            image_src = ""
            try:
                image_element = card.find_element(
                    By.XPATH, XpathConstants.image_element.value
                )
                image_src = image_element.get_attribute("src")
            except Exception as err:
                print(f"Error while finding product Image Url element:{err}")

            product_url = "product url not found."
            try:
                product_url_elem = card.find_element(By.XPATH, XpathConstants.product_url.value)
                product_href = product_url_elem.get_attribute("href")
                # product_href usually already absolute, but just in case:
                if not product_href.startswith("http"):
                    product_url = f"https://www.amazon.com{product_href}"
                else:
                    product_url = product_href
            except Exception as err:
                print(f"Error while finding product Url element:{err}")

            extracted_data = {
                "Product_id": str(uuid4()),
                "Product Name": product_name.strip() if product_name else "Product Name Not Found",
                "Product Price": product_price.strip() if product_price else "Price not found!",
                "Product_rating": product_rating.strip() if product_rating else "Product rating not found",
                "Image_URL": image_src.strip() if image_src else "Image URL Not found.",
                "product url": product_url.strip() if product_url else "product url not found."
            }

            model_item = self.parse_data(extracted_data)
            if not model_item:
                print(f"Could not validate the model data: {model_item}")
                return False

            model_dict = model_item.model_dump()
            data_dict = {
                self.snake_to_title(key): value for key, value in model_dict.items()
            }

            print("Calling the upsert method...")
            print(f"Transformed data_dict: {data_dict}")
            self.airtable_obj.upsert_data(data=data_dict)

            print(f"Data extracted: {extracted_data}")
            return True
        except Exception as err:
            print(f"Error in product details method: {err}")
            return False


def main():
    STATUS = True
    amazon_manager = AmazonCrawler()
    amazon_manager.get_driver()
    amazon_manager.set_cookies()
    
    home_page_response = amazon_manager.request_home_page()
    if not home_page_response:
        print("Home Page Request Failed.")
        return False

    search_field, search_button = amazon_manager.get_search_field()
    if not search_field:
        print("Failed to get the search field.")
        return False

    categories_to_process = AmazonRequestConstants.categories_to_process.value

    for index, category in enumerate(categories_to_process, start=1):
        print(f"\nProcessing category {index} of {len(categories_to_process)}: {category}")

        # Reload home page to avoid stale elements
        amazon_manager.driver.get("https://www.amazon.com")
        WebDriverWait(amazon_manager.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'twotabsearchtextbox')]"))
        )
        search_field, search_button = amazon_manager.get_search_field()
        if not search_field:
            print("Search field not found on reload.")
            continue

        # Reset record flag for this category
        records_present = True
        search_field.clear()
        search_field.send_keys(category)
        search_button.click()

        page_number = 1
        while records_present:
            print(f"Scraping page number: {page_number} for category: {category}")
            cards = amazon_manager.collect_product_cards()
            if not cards:
                print("No product cards found, ending pagination for this category.")
                break

            for idx, card in enumerate(cards, start=1):
                print(f"Processing record {idx} of {len(cards)}")
                amazon_manager.get_product_details(card)

            try:
                next_button = WebDriverWait(amazon_manager.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, XpathConstants.next_page_button.value))
                )
                amazon_manager.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(1)  # Optional small pause
                amazon_manager.driver.execute_script("arguments[0].click();", next_button)
                
                amazon_manager.scroll_page()
                WebDriverWait(amazon_manager.driver, 10).until(
                    EC.staleness_of(cards[0])
                )
                page_number += 1
            except Exception as error:
                print(f"No more pages for this category: {error}")
                break  # Exit pagination for this category

    return True



if __name__ == "__main__":
    main()
