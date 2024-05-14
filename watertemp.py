import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def scrape_website(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <td> elements with class "param"
        param_elements = soup.find_all("td", class_="param")

        # Loop through each <td> element and check if it contains "Temp- 3ft"
        for param_element in param_elements:
            if "Temp- 3ft" in param_element.get("title", ""):
                # Found the "Temp- 3ft" parameter, extract the temperature value
                temperature_value = param_element.find_next_sibling("td", class_="value")
                if temperature_value:
                    temperature = temperature_value.text.strip()
                    print("Temperature:", temperature)
                    
                    # Write temperature to database
                    write_to_database(temperature)
                    return  # Exit the function after finding the temperature value

        # If "Temp- 3ft" parameter not found
        print("Temperature parameter 'Temp- 3ft' not found.")

    except requests.RequestException as e:
        print("Error fetching webpage:", e)

def write_to_database(temperature):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('temperature.db')
        c = conn.cursor()

        # Create a table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS temperature_data
                     (temperature REAL, timestamp TEXT)''')

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert temperature value and timestamp into the table
        c.execute("INSERT INTO temperature_data VALUES (?, ?)", (temperature, timestamp))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("Temperature written to database successfully.")
    except sqlite3.Error as e:
        print("Error writing to database:", e)

# URL of the website to scrape
url = "https://wqdatalive.com/project/applet/html/867?refresh=true"

# Call the scrape_website function with the URL
scrape_website(url)
