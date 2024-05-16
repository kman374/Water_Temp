from feedgen.feed import FeedGenerator
import sqlite3
import hashlib

def generate_guid(content):
    # Generate a unique GUID using a hash of the item's content
    hash_object = hashlib.md5(content.encode())
    return hash_object.hexdigest()

def generate_rss_feed():
    # Initialize FeedGenerator
    fg = FeedGenerator()
    fg.title('Water Temperature RSS Feed')
    fg.link(href='http://example.com', rel='alternate')
    fg.description('RSS feed for water temperature updates')

    # Connect to the SQLite database
    conn = sqlite3.connect('temperature.db')
    c = conn.cursor()

    # Query the database for the latest temperature data
    c.execute("SELECT temperature FROM temperature_data ORDER BY timestamp DESC LIMIT 1")
    latest_temperature = c.fetchone()

    if latest_temperature:
        temperature_value = str(latest_temperature[0]) + '°F'

        # Add the latest temperature as an entry to the feed
        fe = fg.add_entry()
        fe.title(temperature_value)
        fe.guid(generate_guid(temperature_value), permalink=False)  # Set a unique GUID for the entry

    # Close database connection
    conn.close()

    # Generate RSS feed as string
    rss_feed = fg.rss_str(pretty=True)

    # Write the RSS feed to a file
    with open('temperature_feed.xml', 'wb') as f:  # Open the file in binary mode
        f.write(rss_feed)  # Write the bytes to the file

# Generate RSS feed
generate_rss_feed()
