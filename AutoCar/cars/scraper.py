import requests
from bs4 import BeautifulSoup
import logging
import re
import time
import datetime
import json
import os

# Configure more detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_toyota_cars():
    """
    Scrape Toyota car data from AutoDeal Philippines website and save to JSON.
    """
    try:
        # Storage for scraped cars
        cars = []
        
        # First, get the main Toyota page to collect all model links
        base_url = "https://www.autodeal.com.ph"
        main_url = f"{base_url}/cars/toyota"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info(f"Accessing Toyota main page: {main_url}")
        response = requests.get(main_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all model-specific links
        model_links = soup.select('a.darklink.padtop5.ga-tracker')
        logger.info(f"Found {len(model_links)} Toyota models")
        
        # For debugging purposes, limit to just a few models
        # model_links = model_links[:3]  # Uncomment to limit for testing
        
        # For each model, fetch its detailed page
        for link_idx, link in enumerate(model_links):
            try:
                model_url = base_url + link['href']
                model_name = link.text.strip()
                clean_model = model_name.replace('Toyota', '').strip()
                
                logger.info(f"[{link_idx + 1}/{len(model_links)}] Scraping data for: {model_name} at {model_url}")
                
                # Fetch the model-specific page
                model_response = requests.get(model_url, headers=headers)
                model_soup = BeautifulSoup(model_response.content, 'html.parser')
                
                # Save HTML for debugging (first car only)
                if link_idx == 0:
                    with open('debug_page.html', 'w', encoding='utf-8') as f:
                        f.write(model_response.text)
                    logger.info(f"Saved HTML of first car page to debug_page.html for inspection")
                
                # Initialize car data dictionary
                car_data = {
                    'make': 'Toyota',
                    'model': clean_model,
                    'year': datetime.datetime.now().year,
                    'image_url': None,
                    'price': None,
                    'specs': {
                        'body_type': None,
                        'seats': None,
                        'fuel_type': None,
                        'transmission': None,
                        'max_output': None,
                        'drivetrain': None,
                        'wheel_size': None,
                        'airbags': None,
                        'isofix': None,
                        'front_parking_sensors': None,
                        'rear_parking_sensors': None,
                        'connectivity': None,
                        'warranty': None
                    },
                    'features': {
                        'safety': [],
                        'technology': [],
                        'interior': []
                    }
                }
                
                # EXTENSIVE DEBUGGING: Find all tables on the page
                all_tables = model_soup.find_all('table')
                logger.info(f"Found {len(all_tables)} tables on {clean_model} page")
                
                # Examine each table on the page
                for i, table in enumerate(all_tables):
                    rows = table.find_all('tr')
                    logger.info(f"Table {i} has {len(rows)} rows")
                    
                    if len(rows) > 0:
                        # Get table attributes for identification
                        table_class = table.get('class', ['no-class'])
                        logger.info(f"Table {i} class: {table_class}")
                        
                        # Check first row to see if it looks like a spec table
                        first_row = rows[0]
                        cols = first_row.find_all('td')
                        if cols:
                            logger.info(f"Table {i} first row has {len(cols)} columns")
                            if len(cols) >= 2:
                                header = cols[0].text.strip()
                                logger.info(f"Table {i} potential spec label: '{header}'")
                
                # Try to find the specifications table using various methods
                # Method 1: Look for table with product specs container parent
                spec_tables = model_soup.select('.product-specs-container table')
                logger.info(f"Method 1: Found {len(spec_tables)} spec tables with .product-specs-container parent")
                
                # Method 2: Look for tables inside tabs
                tab_tables = model_soup.select('.tab-content table, .tab-pane table')
                logger.info(f"Method 2: Found {len(tab_tables)} tables in tabs")
                
                # Method 3: Look for any table with "specs" in class or parent class
                spec_class_tables = model_soup.select('table[class*=spec], [class*=spec] table')
                logger.info(f"Method 3: Found {len(spec_class_tables)} tables with 'spec' in class")
                
                # Method 4: Look at all tables and find ones that might be spec tables
                potential_spec_tables = []
                for i, table in enumerate(all_tables):
                    rows = table.find_all('tr')
                    if len(rows) > 3:  # At least a few rows
                        first_row = rows[0]
                        cols = first_row.find_all('td')
                        if len(cols) == 2:  # 2 columns is typical for spec tables (label: value)
                            first_label = cols[0].text.strip().lower()
                            # Look for common spec labels
                            if any(keyword in first_label for keyword in ['body', 'engine', 'fuel', 'seats', 'transmission']):
                                potential_spec_tables.append(table)
                
                logger.info(f"Method 4: Found {len(potential_spec_tables)} potential spec tables based on content")
                
                # For the first car, print the first few rows of potential spec tables
                if link_idx == 0 and potential_spec_tables:
                    for i, table in enumerate(potential_spec_tables):
                        logger.info(f"Potential spec table {i} preview:")
                        rows = table.find_all('tr')
                        for j, row in enumerate(rows[:3]):  # First 3 rows
                            cols = row.find_all('td')
                            if len(cols) >= 2:
                                logger.info(f"  Row {j}: '{cols[0].text.strip()}' => '{cols[1].text.strip()}'")
                
                # Combined approach - use any table that worked
                spec_tables = spec_tables or tab_tables or spec_class_tables or potential_spec_tables
                
                if spec_tables:
                    logger.info(f"Processing {len(spec_tables)} spec tables for {clean_model}")
                    
                    # Process each spec table
                    for table in spec_tables:
                        rows = table.find_all('tr')
                        for row in rows:
                            columns = row.find_all('td')
                            if len(columns) >= 2:
                                key = columns[0].text.strip().lower()
                                value = columns[1].text.strip()
                                
                                logger.info(f"Found spec: '{key}' = '{value}'")
                                
                                # Process specific fields
                                if 'body type' in key:
                                    car_data['specs']['body_type'] = value
                                elif 'no. of seats' in key or 'seats' in key:
                                    car_data['specs']['seats'] = re.search(r'\d+', value).group(0) if re.search(r'\d+', value) else value
                                elif 'fuel type' in key:
                                    car_data['specs']['fuel_type'] = value
                                elif 'transmission' in key:
                                    car_data['specs']['transmission'] = value
                                elif 'max output' in key:
                                    car_data['specs']['max_output'] = value
                                    # Also extract the hp number
                                    hp_match = re.search(r'(\d+)\s*hp', value)
                                    if hp_match:
                                        car_data['specs']['horsepower'] = int(hp_match.group(1))
                                elif 'drivetrain' in key:
                                    car_data['specs']['drivetrain'] = value
                                elif 'wheel size' in key:
                                    car_data['specs']['wheel_size'] = value
                                elif 'airbags' in key:
                                    airbag_match = re.search(r'(\d+)', value)
                                    car_data['specs']['airbags'] = int(airbag_match.group(1)) if airbag_match else value
                                elif 'isofix' in key:
                                    car_data['specs']['isofix'] = 'Available' in value
                                elif 'front parking sensors' in key:
                                    car_data['specs']['front_parking_sensors'] = 'Available' in value
                                elif 'rear parking sensors' in key:
                                    car_data['specs']['rear_parking_sensors'] = 'Available' in value
                                elif 'connectivity' in key:
                                    car_data['specs']['connectivity'] = value
                                elif 'warranty' in key:
                                    car_data['specs']['warranty'] = value
                
                # Get the main image
                main_image = model_soup.select_one('.main-image img')
                if main_image and 'src' in main_image.attrs:
                    car_data['image_url'] = main_image['src']
                    logger.info(f"Found image URL: {car_data['image_url']}")
                
                # Get the price range
                # Try different price selectors (h2 span is the primary target)
                price_element = model_soup.select_one('span.h2')
                if not price_element:
                    # Fallback to other potential price containers
                    price_element = model_soup.select_one('.model-price-range, .price-container')

                if price_element:
                    price_text = price_element.text.strip()
                    logger.info(f"Found price text: {price_text}")
                    
                    # Extract all numbers from the text
                    price_matches = re.findall(r'[\d,]+', price_text)
                    if price_matches:
                        # Take the first price as the primary price (usually the starting price)
                        primary_price = float(price_matches[0].replace(',', ''))
                        car_data['price'] = primary_price
                        logger.info(f"Extracted price: {primary_price}")
                        
                        # If there's a range, store the full range too
                        if len(price_matches) > 1:
                            min_price = float(price_matches[0].replace(',', ''))
                            max_price = float(price_matches[-1].replace(',', ''))
                            car_data['price_min'] = min_price
                            car_data['price_max'] = max_price
                            logger.info(f"Price range: {min_price} - {max_price}")
               
                # Add to our collection
                cars.append(car_data)
                logger.info(f"Added car data for: {clean_model}")
                
                # Add a small delay between requests to be polite
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing model {link.get('href', 'unknown')}: {str(e)}")
                continue
        
        # Save all car data to a JSON file
        output_file = 'toyota_cars_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cars, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved data for {len(cars)} cars to {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Toyota car data scraper...")
    result = scrape_toyota_cars()
    if result:
        print("Scraping completed successfully!")
    else:
        print("Scraping failed. Check the log for details.")