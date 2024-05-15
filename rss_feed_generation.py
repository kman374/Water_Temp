from feedgen.feed import FeedGenerator
import sqlite3

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
    c.execute("SELECT temperature, timestamp FROM temperature_data ORDER BY timestamp DESC LIMIT 1")
    latest_data = c.fetchone()

    if latest_data:
        latest_temperature = latest_data[0]
        timestamp = latest_data[1]
        
        # Add the latest temperature as an entry to the feed
        fe = fg.add_entry()
        fe.title(str(latest_temperature) + '°F')
        fe.pubDate(timestamp)  # Set publication date to timestamp

    # Close database connection
    conn.close()

    # Generate RSS feed as string
    rss_feed = fg.rss_str(pretty=True)

    # Write the RSS feed to a file
    with open('temperature_feed.xml', 'w') as f:
        f.write(rss_feed)

# Generate RSS feed
generate_rss_feed()
