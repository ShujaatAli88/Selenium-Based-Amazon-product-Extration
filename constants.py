from enum import Enum


class AmazonRequestUrls(Enum):
    home_page_url = "https://www.amazon.com/"


class AmazonRequestConstants(Enum):
    categories_to_process = [
        "Digital Content & Devices",
        "Shop by Department",
        "Programs & Features",
    ]

    cookies = {
        "session-id": "145-4902261-2194662",
        "session-id-time": "2082787201l",
        "i18n-prefs": "USD",
        "sp-cdn": '"L5Z9:PK"',
        "ubid-main": "131-4180572-4581705",
        "skin": "noskin",
        "session-token": "HKbu/rRDFO/67hrbgAKw1WLYX0Ppxh9biUPLHd15IiSXS9d1McNj5tUNMry6D5sJv1HlsyQXF57kwtQ+5zQu/hp64950WEQO/Q9iAG5xXciMKw04HWL8TD+/rbrPy/z1xY769labzFojm3St+KYAw08BMLTOEAPDcU3Hc9ZFLRvY/Fl1zDXefHl4GxKRF0lV6cPhEs5FNs6xxS5p+rRAv+jwpLtC873zP9T2rVZLcJDwQiGXVQMn7evJnxxNi8lBcl68GM3QBdDrYUISmKOntnaKSXSEMQOVE5d9DzD0Lln30r5vw3W4YnUgkHKRAp9xxSD90A5VAm8N8M94UMYdNU/Mfat8SGyJ",
        "rxc": "ANqE/8c0UQIHoVa3Kmk",
        "csm-hit": "tb:SVB5DVJY072ZDBJ9WW84+s-HKZ7EF7BQZDNYDZ35CSY|1747741452456&t:1747741452457&adb:adblk_no",
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "device-memory": "8",
        "downlink": "10",
        "dpr": "1",
        "ect": "4g",
        "priority": "u=0, i",
        "rtt": "250",
        "sec-ch-device-memory": "8",
        "sec-ch-dpr": "1",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"6.11.0"',
        "sec-ch-viewport-width": "964",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "viewport-width": "964",
    }


class AirTableConstants(Enum):
    TABLE_NAME = "selenium_extracted_data"


class XpathConstants(Enum):
    product_cards = "//div[contains(@role,'listitem')]/div/div"
    product_url = "//a[contains(@class,'a-link-normal s-no-outline')]"
    product_element = ".//h2[@aria-label]"
    product_price = ".//span[@class='a-price']/span[@class='a-offscreen']"
    product_rating = ".//i[@data-cy='reviews-ratings-slot']/span[@class='a-icon-alt']"
    image_element = ".//div[contains(@class,'a-section aok-relative s-image-fixed-height')]/img[contains(@class,'s-image')]"
    pagination_element = "//span[contains(@class,'s-pagination-item s-pagination-previous s-pagination-disabled ')]"
    next_page_button = "//li[contains(@class,'s-list-item-margin-right-adjustment')]/span/a[contains(text(),'Next')]"
