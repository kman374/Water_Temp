import requests
from bs4 import BeautifulSoup

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
                    print("Temperature:", temperature_value.text.strip())
                    return  # Exit the function after finding the temperature value

        # If "Temp- 3ft" parameter not found
        print("Temperature parameter 'Temp- 3ft' not found.")

    except requests.RequestException as e:
        print("Error fetching webpage:", e)

# URL of the website to scrape
url = "https://wqdatalive.com/project/applet/html/867?refresh=true"

# Call the scrape_website function with the URL
scrape_website(url)
