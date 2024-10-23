import json
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class RestaurantScraper:
    def __init__(self):
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Initialize the Chrome driver with wait"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def get_restaurant_details(self, restaurant_element):
        """Extract detailed information for a single restaurant"""
        try:
            # Click on the restaurant to open details
            restaurant_element.click()
            time.sleep(2)  # Wait for details to load

            details = {}

            # Get the container of the restaurant details
            restaurant_container = restaurant_element.find_element(By.XPATH, "..")

            # Get basic information
            name = restaurant_element.get_attribute("aria-label").removesuffix(" · Visited link")
            details['name'] = name
            # details['name'] = restaurant_element.get_attribute("aria-label").rstrip("Visited link")

            # Get description
            try:
                description_elem = self.driver.find_element(By.XPATH, ".//div[@class='PYvSYb ']")
                details['description'] = description_elem.text
            except NoSuchElementException:
                details['description'] = "Description not available"

            # Get rating
            try:
                rating_elem = restaurant_container.find_element(By.XPATH, ".//span[@class='MW4etd']")
                details['rating'] = rating_elem.text
            except NoSuchElementException:
                details['rating'] = "No rating available"

            # Get number of reviews
            try:
                reviews_elem = restaurant_container.find_element(By.XPATH, "//span[contains(@aria-label,'reviews')]")
                details['review_count'] = reviews_elem.text.replace('(', '').replace(')', '')
            except NoSuchElementException:
                details['review_count'] = "No reviews available"

            # Get address
            try:
                address_elem = restaurant_container.find_element(By.XPATH, "//button[@class='CsEnBe']")
                details['address'] = address_elem.get_attribute("aria-label")
            except NoSuchElementException:
                details['address'] = "Address not available"

            # Get cuisine type
            try:
                cuisine_elem = restaurant_container.find_element(By.XPATH, "//button[@class='DkEaL ']")
                details['cuisine'] = cuisine_elem.text
            except NoSuchElementException:
                details['cuisine'] = "Cuisine type not available"

            # Get price level
            try:
                price_elem = restaurant_container.find_element(By.XPATH, ".//span[contains(@aria-label,'Price')]")
                details['price_level'] = price_elem.text
            except NoSuchElementException:
                details['price_level'] = "Price level not available"

            return details

        except Exception as e:
            print(f"Error getting restaurant details: {e}")
            return None

    def google_search_restaurants(self, city):
        """Main function to search and scrape restaurant data"""
        try:
            self.setup_driver()

            # Go to Google Search
            self.driver.get("https://www.google.com")

            # Search for restaurants
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            query = f"Top 10 restaurants in {city}"
            search_box.send_keys(query)
            search_box.send_keys("\n")
            print(f"Searching for: {query}")

            # Click on Maps
            maps_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Maps']")))
            maps_button.click()
            print("\n⏳ Please wait while the scraper collects restaurant details...")
            print("This process might take a few minutes to ensure accurate data collection.\n")

            restaurants = {}
            scroll_attempts = 0

            while len(restaurants) < 10 and scroll_attempts < 15:
                # Find restaurant elements
                restaurant_elements = self.wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[@class='hfpxzc']"))
                )

                for restaurant in restaurant_elements:
                    if len(restaurants) >= 10:
                        break

                    details = self.get_restaurant_details(restaurant)
                    if details and details['name'] not in restaurants:
                        restaurants[details['name']] = details

                # Scroll to load more results
                if len(restaurants) < 10:
                    last_element = restaurant_elements[-1]
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true); window.scrollBy(0, 200);",
                        last_element
                    )
                    time.sleep(2)

                scroll_attempts += 1

            # Save data to JSON file with city name and timestamp
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{city}_restaurants_{timestamp}.json"

            with open(filename, "w", encoding='utf-8') as file:
                json.dump(restaurants, file, indent=4, ensure_ascii=False)

            print(f"Successfully scraped {len(restaurants)} restaurants")
            print(f"Data saved to {filename}")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            if self.driver:
                self.driver.quit()

def main():
    while True:
        city = input("Enter the city name (or 'quit' to exit): ").strip()
        if city.lower() == 'quit':
            break

        scraper = RestaurantScraper()
        scraper.google_search_restaurants(city)

if __name__ == "__main__":
    main()